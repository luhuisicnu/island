from celery.task import task

from django.conf import settings
from .models import Level


@task(ignore_result=True)
def refresh_level_name():
    """刷新用户等级"""
    def do_refresh(query_set, level_name):
        for level in query_set.all():
            if level.description != level_name:
                level.description = level_name
                level.save()

    all_levels = Level.objects.order_by('-integral')
    level9 = all_levels[:settings.TOP_LEVEL_USER_LIMIT]
    if not level9.exists():
        return
    do_refresh(level9, settings.LEVEL_NAME[9])
    level8 = all_levels[settings.TOP_LEVEL_USER_LIMIT:settings.NEXT_LEVEL_USER_LIMIT]
    if not level8.exists():
        return
    do_refresh(level8, settings.LEVEL_NAME[8])

    other_levels = all_levels[settings.NEXT_LEVEL_USER_LIMIT:]
    if not other_levels.exists():
        return
    other_max_integral = other_levels[0].integral
    level7_integral = int(other_max_integral * settings.OTHER_LEVEL_INTERGRAL_LIMIT[-1])
    level6_integral = int(other_max_integral * settings.OTHER_LEVEL_INTERGRAL_LIMIT[-2])
    level5_integral = int(other_max_integral * settings.OTHER_LEVEL_INTERGRAL_LIMIT[-3])
    level4_integral = int(other_max_integral * settings.OTHER_LEVEL_INTERGRAL_LIMIT[-4])
    level3_integral = int(other_max_integral * settings.OTHER_LEVEL_INTERGRAL_LIMIT[-5])
    level2_integral = int(other_max_integral * settings.OTHER_LEVEL_INTERGRAL_LIMIT[-6])
    level1_integral = int(other_max_integral * settings.OTHER_LEVEL_INTERGRAL_LIMIT[-7])
    level0_integral = 0

    for floor_integral, ceil_integral, index in [
        (level7_integral, other_max_integral, 7),
        (level6_integral, level7_integral, 6),
        (level5_integral, level6_integral, 5),
        (level4_integral, level5_integral, 4),
        (level3_integral, level4_integral, 3),
        (level2_integral, level3_integral, 2),
        (level1_integral, level2_integral, 1),
        (level0_integral, level1_integral, 0),
    ]:
        levels = all_levels.filter(integral__gte=floor_integral, integral__lt=ceil_integral)
        do_refresh(levels, settings.LEVEL_NAME[index])

