# coding=utf-8
from tests.utils.json_utils import SectionAPI

found_count = SectionAPI().get_sections()
for super_section in found_count:
    print '' + super_section['name']
    for section in super_section['sections']:
        print '     ' + section['name']
        for category in section['categories']:
            print '         ' + category['name']


# //span[@class="ng-binding" and text()="События"]