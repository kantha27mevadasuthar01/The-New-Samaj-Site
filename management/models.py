from django.db import models
from django.utils.translation import gettext_lazy as _

class CommitteeSettings(models.Model):
    """
    Stores global settings for the committee, such as the current term years.
    This model should typically have only one instance.
    """
    start_year = models.PositiveIntegerField(_("Start Year"), default=2025)
    end_year = models.PositiveIntegerField(_("End Year"), default=2026)

    class Meta:
        verbose_name = _("Committee Settings")
        verbose_name_plural = _("Committee Settings")

    def __str__(self):
        return f"Term: {self.start_year} - {self.end_year}"

class CommitteeMember(models.Model):
    """
    Represents a member of the Executive Committee.
    Includes predefined positions with limits on the number of members per position.
    """
    POSITIONS = [
        ('PRAMUKH', _('Pramukh')),
        ('UP_PRAMUKH', _('Up-pramukh')),
        ('MANTRI', _('Mantri')),
        ('SAH_MANTRI', _('Sah-Mantri')),
        ('KHAJANCHI', _('Khajanchi')),
        ('SAMAJIK_CONVENER', _('Samajik Convener')),
        ('ARTHIC_CONVENER', _('Arthic Convener')),
        ('SHAIKSHANIK_CONVENER', _('Shaikshanik Convener')),
        ('KAROBARI_SABHY', _('Karobari Sabhy')),
        ('AUDITOR', _('Extra Auditor')),
    ]

    POSITION_LIMITS = {
        'PRAMUKH': 1,
        'UP_PRAMUKH': 1,
        'MANTRI': 1,
        'SAH_MANTRI': 1,
        'KHAJANCHI': 1,
        'SAMAJIK_CONVENER': 4,
        'ARTHIC_CONVENER': 4,
        'SHAIKSHANIK_CONVENER': 6,
        'KAROBARI_SABHY': 27,
        'AUDITOR': 1,
    }

    name = models.CharField(_("Name"), max_length=200)
    designation = models.CharField(_("Designation"), max_length=50, choices=POSITIONS)
    village = models.CharField(_("Village"), max_length=100)
    mobile_number = models.CharField(_("Mobile Number"), max_length=15)
    display_order = models.PositiveIntegerField(_("Display Order"), default=0)
    person = models.ForeignKey('people.Person', on_delete=models.SET_NULL, null=True, blank=True, related_name='committee_memberships')
    
    class Meta:
        verbose_name = _("Committee Member")
        verbose_name_plural = _("Committee Members")
        ordering = ['display_order', 'name']

    def __str__(self):
        return f"{self.name} - {self.get_designation_display()}"
    
    @classmethod
    def get_total_members(cls):
        """Get total number of committee members"""
        return cls.objects.count()
    
    @classmethod
    def is_committee_full(cls):
        """Check if committee has reached 47-member limit"""
        return cls.get_total_members() >= 47
    
    @classmethod
    def get_available_positions(cls):
        """Get positions that still have available slots"""
        available = []
        for position_code, position_name in cls.POSITIONS:
            current_count = cls.objects.filter(designation=position_code).count()
            limit = cls.POSITION_LIMITS.get(position_code, 0)
            if current_count < limit:
                available.append((position_code, position_name, limit - current_count))
        return available
    
    @classmethod
    def get_available_slots(cls):
        """Get number of remaining slots out of 47"""
        return 47 - cls.get_total_members()
