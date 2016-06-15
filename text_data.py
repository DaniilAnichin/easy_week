import gettext

eng = gettext.translation('easy_week', './locale', languages=['en'])
ua = gettext.translation('easy_week', './locale', languages=['ua'])
ru = gettext.translation('easy_week', './locale', languages=['ru'])

ua.install()

# Data which will form the view of popup, e.g. label, button text
data_group = {
    'title': _('Group schedule'),
    'btn_text': _('Choose group cypher')
}
data_teacher = {
    'title': _('Teacher schedule'),
    'btn_text': _('Choose teacher')
}
data_room = {
    'title': _('Room schedule'),
    'btn_text': _('Choose room number')
}
popup_data = {
    'group': data_group,
    'teacher': data_teacher,
    'room': data_room
}

# Data which will form the view of pair, e.g. week days, time lapse
day_times = [
    '08:30 - 10:05',
    '10:25 - 12:00',
    '12:20 - 13:55',
    '14:15 - 15:50',
    '16:10 - 17:45'
]
lesson_types = {
    'lect': _('Lecture'),
    'pract': _('Practice'),
    'lab': _('Laboratory')
}
week_types = {
    'upper': 'I',
    'lower': 'II'
}
week_days = [
    _('Monday'),
    _('Tuesday'),
    _('Wednesday'),
    _('Thursday'),
    _('Friday'),
    _('Saturday'),
    _('Sunday')
]
# Test data for lessons, just example
data_lesson = [
    dict(
        teacher='Orlovskiy I.V.', lesson='High Math II', type='lect',
        groups=['IK-51', 'IK-52'], room='18/413', week='upper', day=1, number=1
    ), dict(
        teacher='Lisovichenko O.I.', lesson='OOP', type='pract',
        groups=['IK-51'], room='18/438', week='lower', day=4, number=3
    )
]


def lesson_to_str(lesson):
    if lesson.empty():
        return ''
    result = '%s' % lesson.lesson.decode('utf-8')[:12].encode('utf-8')
    if len(lesson.lesson.decode('utf-8')) > 12:
        result += '...'
    # result += '\n%s' % lesson_types[lesson.type]
    if not lesson.view_type.startswith('teacher'):
        result += '\n%s' % lesson.teacher.decode('utf-8')[:12].encode('utf-8')
        if len(lesson.teacher.decode('utf-8')) > 12:
            result += '...'
    if not lesson.view_type.startswith('room'):
        result += _('\nIn %s room') % lesson.room
    if not lesson.view_type.startswith('group'):
        groups = ', '.join(lesson.groups)
        result += '\n%s' % groups[:14] + ('...' if len(groups) > 17 else '')
    return result
