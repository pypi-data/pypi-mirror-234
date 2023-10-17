from datetime import datetime, timedelta, timezone

from eveuniverse.models import EveSolarSystem

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class Wormhole(models.Model):

    class Complexes(models.TextChoices):
        """"
        The Various Drifter Complexes that a hole can lead to
        """
        BARBICAN = 'Barbican', _("Barbican")
        CONFLUX = 'Conflux', _("Conflux")
        REDOUBT = 'Redoubt', _("Redoubt")
        SENTINEL = 'Sentinel', _("Sentinel")
        VIDETTE = 'Vidette', _("Vidette")

    class Mass(models.TextChoices):
        """"
        The states of Mass remaining
        """
        FRESH = 'Fresh', _(
            "This wormhole has not yet had its stability significantly disrupted by ships passing through it")  # >50%
        REDUCED = 'Reduced', _(
            "This wormhole has had its stability reduced by ships passing through it, but not to a critical degree yet")  # <50, >10%
        CRIT = 'Critical', _(
            "This wormhole has had its stability critically disrupted by the mass of numerous ships passing through and is on the verge of collapse")  # <10%

    class Lifetime(models.TextChoices):
        """"
        The states of Time Remaining
        """
        FRESH = 'Fresh', _(
            "This wormhole has not yet begun its natural cycle of decay and should last at least another day")   # >24 Hours?
        DECAY = 'Decaying', _(
            "This wormhole is beginning to decay, and probably won't last another day")  # <24h
        EOL = 'EOL', _("This wormhole is reaching the end of its natural lifetime")  # <4h

    system = models.ForeignKey(EveSolarSystem, verbose_name=_("Solar System"), on_delete=models.CASCADE)
    complex = models.CharField(_("Complex"), max_length=50, choices=Complexes.choices)
    mass = models.CharField(_("Mass Remaining"), max_length=50, choices=Mass.choices)
    bookmarked_k = models.BooleanField(_("K Space Bookmarked"))
    bookmarked_w = models.BooleanField(_("W Space Bookmarked"))

    lifetime = models.CharField(_("Lifetime Remaining"), max_length=50, choices=Lifetime.choices)
    eol_changed_at = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True, null=True,)

    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    created_by = models.ForeignKey(User, verbose_name=_(
        ""), on_delete=models.CASCADE, null=True, blank=True, related_name="+")

    updated_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_by = models.ForeignKey(User, verbose_name=_(
        ""), on_delete=models.CASCADE, null=True, blank=True, related_name="+")

    archived = models.BooleanField(_("Archived"), blank=True, null=True, default=False)
    archived_at = models.DateTimeField(blank=True, null=True)
    archived_by = models.ForeignKey(User, verbose_name=_(
        ""), on_delete=models.CASCADE, null=True, blank=True, related_name="+")

    class Meta:
        verbose_name = _("Wormhole")
        verbose_name_plural = _("Wormholes")

    def __str__(self):
        return f"{self.system.name} - {self.complex}"

    def set_eol(self) -> bool:
        """
        Set a wormhole as EOL, updating the eol_changed_at timestamp

        :return: Set EOL? False if not set or already EOL
        :rtype: bool
        """
        if self.lifetime == 'Decaying':
            self.eol_changed_at = datetime.now(timezone.utc)
            self.lifetime = 'EOL'
            self.save
            return True
        return False

    @property
    def age(self) -> timedelta:
        return self.created_at - datetime.now(timezone.utc)

    @property
    def time_since_update(self) -> timedelta:
        return self.updated_at - datetime.now(timezone.utc)

    @property
    def time_since_eol(self) -> timedelta:
        return self.eol_changed_at - datetime.now(timezone.utc)

    @property
    def formatted_lifetime(self) -> str:
        if self.lifetime == 'Decaying':
            return f"{self.lifetime} {self.age.total_seconds() / timedelta(hours=16).total_seconds():.2%}"
        elif self.eol_changed_at is None and self.lifetime == 'EOL':
            return f"{self.lifetime} {self.age.total_seconds() / timedelta(hours=4).total_seconds():.2%}"
        elif self.eol_changed_at is not None and self.lifetime == 'EOL':
            return f"{self.lifetime} {self.time_since_eol.total_seconds() / timedelta(hours=4).total_seconds():.2%}"
        return "N/A"


class Clear(models.Model):

    system = models.ForeignKey(EveSolarSystem, verbose_name=_("Solar System"), on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, verbose_name=_(
        ""), on_delete=models.CASCADE, null=True, blank=True, related_name="+")

    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, verbose_name=_(
        ""), on_delete=models.CASCADE, null=True, blank=True, related_name="+")

    class Meta:
        verbose_name = _("Wormhole")
        verbose_name_plural = _("Wormholes")

    def __str__(self):
        return f"{self.system.name} - CLEAR"

    @property
    def age(self) -> timedelta:
        return self.created_at - datetime.now(timezone.utc)

    @property
    def time_since_update(self) -> timedelta:
        return datetime.now(timezone.utc) - self.updated_at
