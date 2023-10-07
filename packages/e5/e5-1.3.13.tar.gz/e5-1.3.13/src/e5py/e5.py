# ## E5 by Shannon McPherron
#
#   This is a beta release.  I am still working on bugs and I am still implementing some features.
#   But it has been used to collect data and seems to work in most cases.  Caution should be exercised.
#   It should be backwards compatible with E4 and Entrer Trois (but there are still some issues).
#   A Windows version is available here, and has been tested on Windows 10.  Older versions of Windows
#   will likely experience issues.  This code also works on Mac and Linux.

# ToDo and Bugs:
#   If TYPE is missing from CFG provide a default of text
#   Fix box on icon
#   Make a loading icon
#   Set icon on program main screen
#   Add better formatted note and GPS fields to edit last record and data grid
#   Find a way to note when you are on the first field
#   Ask whether to add to menulist when new item is entered
#   Somehow show info from last record entered on first screen
#   Look into letting user set CSV file save name
#   Test species menu
#   Handle database and table names in the CFG and program better
#   On unique fields, give a warning but let data entry continue
#   then overwrite previous record
#   Implement 'sort' option on menus
#   Key press on boolean moves to right menu item but adds key press too
#   Add a CFG option to sort menus
#   Don't let it re-write the CFG if there are errors - can trash a cfg that is not an E5/E4 cfg

# Long term
#   Consider putting a dropdown menu into the grid view for sorting and maybe searching
#   Think about whether to allow editing of CFG in the program

# Version 1.3.11
#  Brought in all changes made to EDMpy interface
#  Fixed issue with parsing conditions - matches starting with NOT did not work (e.g. NOTCH)
#  Put classes into separate files

# Version 1.3.12
#  Moved fixes done in EDM over to E5 (should resolve a Mac formatting issue as well)
#  Resolved a ton of data entry issues mostly related to keyboard entry

# Version 1.3.13
#   Fixed UNIQUE issue
#   Fixed one glitch in enter key

# TODO Need to fix ASAP conditions in e4 not comma delimited

__version__ = '1.3.13'
__date__ = 'October, 2023'
__program__ = 'E5'

from kivy.config import Config
from kivy import resources
from kivy.clock import Clock, mainthread
from kivy.app import App
from kivy.uix.switch import Switch
from kivy.factory import Factory
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy import __version__ as __kivy_version__

# The explicit mention of this package here
# triggers its inclusions in the pyinstaller spec file.
# It is needed for the filechooser widget.
try:
    import win32timezone
    win32timezone.TimeZoneInfo.local()
except ModuleNotFoundError:
    pass

import sys
from os import path
from random import random
from platform import python_version

from plyer import gps
from plyer import camera
from plyer import __version__ as __plyer_version__

import logging
from appdata import AppDataPaths

# My libraries for this project
from e5py.lib.dbs import dbs
from e5py.lib.e5_widgets import e5_MainScreen, e5_scrollview_menu, e5_scrollview_label, e5_button, e5_label, e5_side_by_side_buttons, e5_LoadDialog, e5_MessageBox, e5_textinput, e5_RecordEditScreen
from e5py.lib.e5_widgets import e5_DatagridScreen, e5_InfoScreen, e5_LogScreen, e5_CFGScreen, e5_INIScreen, e5_SettingsScreen, DataUploadScreen
from e5py.lib.colorscheme import ColorScheme
from e5py.lib.misc import platform_name, restore_window_size_position, filename_only
from e5py.constants import APP_NAME
from e5py.cfg import cfg
from e5py.ini import ini

# The database - pure Python
from tinydb import __version__ as __tinydb_version__


class db(dbs):
    MAX_FIELDS = 300
    datagrid_doc_id = None


class MainScreen(e5_MainScreen):

    gps_location = StringProperty(None)
    gps_location_widget = ObjectProperty(None)
    gps_status = StringProperty('Click Start to get GPS location updates')

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)

        self.setup_logger()

        self.colors = ColorScheme()
        self.ini = ini()
        self.cfg = cfg()
        self.data = db()
        self.warnings, self.errors = self.setup_program()

        if platform_name() == 'Android':
            self.colors.button_font_size = "14sp"

        # Used for KV file settings
        self.text_color = self.colors.text_color
        self.button_color = self.colors.button_color
        self.button_background = self.colors.button_background

        self.fpath = ''

        if self.cfg.gps:
            logger = logging.getLogger(__name__)
            try:
                logger.info('Configuring GPS in mainscreen')
                gps.configure(on_location=self.on_gps_location,
                              on_status=self.on_gps_status)
            except (NotImplementedError, ModuleNotFoundError):
                logger.info('Error configuring GPS in mainscreen')
                self.gps_status = 'GPS is not implemented for your platform'

        self.mainscreen = BoxLayout(orientation='vertical',
                                    size_hint_y=.9,
                                    size_hint_x=.8,
                                    pos_hint={'center_x': .5},
                                    padding=20,
                                    spacing=20)
        self.add_widget(self.mainscreen)
        self.build_mainscreen()
        self.add_screens()
        restore_window_size_position(__program__, self.ini)
        self.if_camera_setup_camera()

    def setup_logger(self):
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh = logging.FileHandler(self.app_paths.log_file_path)
        fh.setLevel(logging.INFO)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        logger.info(__program__ + ' started, logger initialized, and application built.')

    def update_title(self):
        for widget in self.walk():
            if hasattr(widget, 'action_previous'):
                widget.action_previous.title = 'E5'
                if self.cfg is not None:
                    if self.cfg.filename:
                        widget.action_previous.title = filename_only(self.cfg.filename)

    def add_screens(self):
        sm.add_widget(StatusScreen(name='StatusScreen',
                                    colors=self.colors,
                                    e5_cfg=self.cfg,
                                    e5_ini=self.ini,
                                    e5_data=self.data))
        sm.add_widget(e5_LogScreen(name='LogScreen',
                                    colors=self.colors,
                                    logger=logging.getLogger(__name__)))
        sm.add_widget(e5_CFGScreen(name='CFGScreen',
                                    colors=self.colors,
                                    cfg=self.cfg))
        sm.add_widget(e5_INIScreen(name='INIScreen',
                                    colors=self.colors,
                                    ini=self.ini))
        sm.add_widget(AboutScreen(name='AboutScreen',
                                        colors=self.colors))
        sm.add_widget(DataUploadScreen(name='UploadScreen',
                                        data=self.data,
                                        cfg=self.cfg,
                                        colors=self.colors))
        sm.add_widget(EditLastRecordScreen(name='EditLastRecordScreen',
                                            data=self.data,
                                            doc_id=None,
                                            e5_cfg=self.cfg,
                                            colors=self.colors))
        sm.add_widget(EditPointsScreen(name='EditPointsScreen',
                                        colors=self.colors,
                                        main_data=self.data,
                                        main_tablename=self.data.table if self.data else '_default',
                                        main_cfg=self.cfg))
        sm.add_widget(EditCFGScreen(name='EditCFGScreen',
                                    colors=self.colors,
                                    e5_cfg=self.cfg))
        sm.add_widget(e5_SettingsScreen(name='E5SettingsScreen',
                                        colors=self.colors,
                                        ini=self.ini,
                                        cfg=self.cfg))

    @mainthread
    def on_gps_location(self, **kwargs):
        results, linefeed = '', ''
        for k, v in kwargs.items():
            results += linefeed + k.capitalize() + ' = '
            results += '%s' % (v if k != 'accuracy' else round(float(v), 3))
            linefeed = '\n'
        self.gps_location_widget.text = results

    @mainthread
    def on_gps_status(self, stype, status):
        logger = logging.getLogger(__name__)
        logger.info('GPS status updated.')
        self.gps_status = 'type={}\n{}'.format(stype, status)
        status = self.get_widget_by_id('gps_status')
        if status:
            status.text = self.gps_status

    def on_enter(self):
        self.build_mainscreen()

    def reset_screens(self):
        for screen in sm.screens[:]:
            if screen.name != 'MainScreen':
                sm.remove_widget(screen)
        self.add_screens()

    def build_mainscreen(self):

        self.mainscreen.clear_widgets()
        self.scroll_menu = None

        if self.cfg.filename:
            self.cfg.start()
            if not self.cfg.EOF or not self.cfg.BOF:
                self.data_entry()
                if self.cfg.has_warnings:
                    self.event = Clock.schedule_once(self.show_popup_message, 1)
            else:
                self.cfg_menu()
                self.event = Clock.schedule_once(self.show_popup_message, 1)

        else:
            if self.ini.first_time:
                self.ini.first_time = False
                self.event = Clock.schedule_once(self.show_popup_message, 1)
            self.cfg_menu()
        self.update_title()

    def if_camera_setup_camera(self):
        if self.cfg.camera_in_cfg():
            try:
                self.camera = camera.Camera(play=True, size_hint_y=.8, resolution=(-1, -1))
            except Exception as e:
                print("Oops!", e.__class__, "occurred.")
                self.camera = None
        else:
            self.camera = None

    def cfg_menu(self):

        self.cfg_files = self.get_files(self.get_path(), 'cfg')

        if self.cfg_files:

            self.cfg_file_selected = self.cfg_files[0]

            lb = Label(text='Begin data entry with one of these CFG files or use File Open',
                        color=self.colors.text_color,
                        size_hint_y=.1)
            self.mainscreen.add_widget(lb)

            self.mainscreen.add_widget(e5_scrollview_menu(self.cfg_files,
                                                            self.cfg_file_selected,
                                                            widget_id='cfg',
                                                            call_back=[self.cfg_selected],
                                                            colors=self.colors))
            self.scroll_menu = self.get_widget_by_id('cfg_scroll')
            self.scroll_menu.make_scroll_menu_item_visible()
            self.widget_with_focus = self.scroll_menu

        else:
            label_text = '\nBefore data entry can begin, you need to have a CFG file.\n\nThe current folder %s contains none.  Either use File Open to switch a folder that contains CFG files or create a new one.' % self.get_path()
            lb = e5_scrollview_label(text=label_text, id='label', colors=self.colors)
            lb.halign = 'center'
            self.mainscreen.add_widget(lb)
            self.widget_with_focus = self.mainscreen

    def cfg_selected(self, value):
        if value.text:
            self.load_cfg(path.join(self.get_path(), value.text))

    def load_cfg(self, cfgfile_name):
        self.data.close()
        self.cfg.load(cfgfile_name)
        if self.cfg.filename:
            self.open_db()
            self.set_new_data_to_true()
        self.ini.update(self.colors, self.cfg)
        self.build_mainscreen()
        self.reset_screens()
        self.if_camera_setup_camera()

    def set_new_data_to_true(self, table_name=None):
        if table_name is None:
            self.data.new_data[self.data.table] = True
        else:
            self.data.new_data[table_name] = True

    def data_entry(self):

        if platform_name() == 'Android':
            size_hints = {'field_label': .13,
                            'field_input': .07 if not self.cfg.current_field.inputtype == 'NOTE' else .07 * 5,
                            'scroll_content': .6 if not self.cfg.current_field.inputtype == 'NOTE' else .6 - .07 * 4,
                            'prev_next_buttons': .2}
        else:
            size_hints = {'field_label': .13,
                            'field_input': .07 if not self.cfg.current_field.inputtype == 'NOTE' else .07 * 5,
                            'scroll_content': .6 if not self.cfg.current_field.inputtype == 'NOTE' else .6 - .07 * 4,
                            'prev_next_buttons': .2}

        # mainscreen = self.get_widget_by_id('mainscreen')
        # inputbox.bind(minimum_height = inputbox.setter('height'))
        # print(self.cfg.current_record)

        label = e5_label(text=self.cfg.current_field.prompt,
                            size_hint=(1, size_hints['field_label']),
                            color=self.colors.text_color,
                            id='field_prompt',
                            halign='center')
        if self.colors:
            if self.colors.text_font_size:
                label.font_size = self.colors.text_font_size
        self.mainscreen.add_widget(label)
        label.bind(texture_size=label.setter('size'))
        label.bind(size_hint_min_x=label.setter('width'))

        self.field_data = e5_textinput(text=self.cfg.current_record[self.cfg.current_field.name] if self.cfg.current_field.name in self.cfg.current_record.keys() else '',
                                        size_hint=(1, size_hints['field_input']),
                                        multiline=(self.cfg.current_field.inputtype == 'NOTE'),
                                        input_filter=None if self.cfg.current_field.inputtype not in ['NUMERIC', 'INSTRUMENT'] else 'float',
                                        write_tab=False,
                                        id='field_data')
        if self.colors:
            if self.colors.text_font_size:
                self.field_data.textbox.font_size = self.colors.text_font_size
        self.mainscreen.add_widget(self.field_data)
        self.field_data.textbox.bind(text=self.textbox_changed)
        self.widget_with_focus = self.field_data.textbox
        self.field_data.textbox.focus = True

        self.scroll_menu = None
        self.scroll_content = BoxLayout(orientation='horizontal',
                                        size_hint=(1, size_hints['scroll_content']),
                                        spacing=20)
        self.add_scroll_content(self.scroll_content, self.field_data.textbox.text)

        if self.cfg.current_field.inputtype in ['BOOLEAN', 'MENU']:
            self.scroll_menu_setup()

        buttons = GridLayout(cols=2, size_hint=(1, size_hints['prev_next_buttons']), spacing=20)

        buttons.add_widget(e5_button('Back', id='back', selected=True,
                                     call_back=self.go_back, colors=self.colors))

        buttons.add_widget(e5_button('Next', id='next', selected=True,
                                     call_back=self.go_next, colors=self.colors))

        if platform_name() == 'Android':
            self.mainscreen.add_widget(buttons)
            self.mainscreen.add_widget(self.scroll_content)
        else:
            self.mainscreen.add_widget(self.scroll_content)
            self.mainscreen.add_widget(buttons)

        self.field_data.textbox.select_all()
        self.event = Clock.schedule_once(self.field_data_set_focus, .1)

    def field_data_set_focus(self, dt):
        self.field_data.textbox.focus = True
        self.field_data.textbox.select_all()

    def scroll_menu_setup(self):
        if self.scroll_menu is not None:
            self.scroll_menu.make_scroll_menu_item_visible()
        self.widget_with_focus = self.scroll_menu if self.scroll_menu else self

    def textbox_changed(self, instance, value):
        if self.cfg.current_field.inputtype in ['BOOLEAN', 'MENU']:
            self.add_scroll_content(self.scroll_content, value)
            self.scroll_menu_setup()

    # def _keyboard_closed(self):
    #    self._keyboard.unbind(on_key_down = self._on_keyboard_down)
    #    self._keyboard = None

    def _on_keyboard_down(self, *args):
        if self.parent:
            if self.parent.current == 'MainScreen':
                ascii_code = args[1]
                text_str = args[3]
                # print('INFO: The key %s has been pressed %s' % (ascii_code, text_str))
                if not self.popup_open:
                    if ascii_code in [8, 127]:
                        return False
                    if ascii_code == 9:
                        if self.widget_with_focus.id == 'menu_scroll':
                            self.widget_with_focus = self.field_data.textbox
                            self.widget_with_focus.focus = True
                        elif self.widget_with_focus.id == 'field_data' and self.cfg.current_field.inputtype in ['MENU', 'BOOLEAN']:
                            self.widget_with_focus.focus = False
                            self.widget_with_focus = self.get_widget_by_id('menu_scroll')
                        return False
                    if ascii_code == 27:
                        if self.cfg.filename:
                            self.go_back(None)
                    if ascii_code == 13:
                        if self.cfg.filename:
                            self.go_next(None)
                            return True
                        elif self.cfg_files:
                            self.cfg_selected(self.scroll_menu.scroll_menu_get_selected())
                    if ascii_code == 51:
                        return True
                    if ascii_code in [273, 274, 275, 276, 278, 279] and self.scroll_menu:
                        self.scroll_menu.move_scroll_menu_item(ascii_code)
                        return False
                    if ascii_code in [276, 275, 278, 279] and not self.scroll_menu:
                        return False
                    # if 'ctrl' in args[4] and args[3] == 'c':
                    #    Clipboard.copy(self.field_data.text)
                    # if 'ctrl' in args[4] and args[3] == 'v':
                    #    self.field_data.text = Clipboard.paste()
                    # if text_str:
                    #    if text_str.upper() in ascii_uppercase:
                    #        self.add_scroll_content(self.get_widget_by_id('scroll_content'),
                    #                                self.get_widget_by_id('field_data').text + text_str)
                    #        return True
                else:
                    if ascii_code == 13:
                        self.close_popup(None)
                        self.widget_with_focus.focus = True
                        return True
                    elif ascii_code in [275, 276]:
                        return False
                return False  # return True to accept the key. Otherwise, it will be used by the system.
        else:
            return False

    def copy_from_menu_to_textbox(self):
        if self.cfg.current_field.inputtype in ['MENU', 'BOOLEAN']:
            textbox = self.field_data.textbox.text
            menubox = self.scroll_menu.scroll_menu_get_selected().text if self.scroll_menu.scroll_menu_get_selected() else ''
            if textbox == '' and not menubox == '':
                self.field_data.textbox.text = menubox
            elif not textbox == '' and not menubox == '':
                if not textbox.upper() == menubox.upper():
                    if textbox.upper() == menubox.upper()[0:len(textbox)]:
                        self.field_data.textbox.text = menubox
                else:
                    self.field_data.textbox.text = menubox

    def copy_from_gps_to_textbox(self):
        if self.cfg.current_field.inputtype in ['GPS']:
            textbox = self.field_data.textbox
            textbox.text = self.gps_location_widget.text.replace('\n', ',')

    def add_scroll_content(self, content_area, menu_filter=''):

        content_area.clear_widgets()

        info_exists = self.cfg.current_field.info or self.cfg.current_field.infofile
        menu_exists = self.cfg.current_field.inputtype == 'BOOLEAN' or (not self.cfg.current_field.menu == [])
        camera_exists = self.cfg.current_field.inputtype == 'CAMERA'
        gps_exists = self.cfg.current_field.inputtype == 'GPS'

        if menu_exists or info_exists or camera_exists or gps_exists:

            if camera_exists:
                if self.camera is not None:
                    if self.camera.parent is not None:
                        self.camera.parent.remove_widget(self.camera)
                bx = BoxLayout(orientation='vertical')
                # bx.add_widget(self.camera)
                # self.camera.play = True
                bx.add_widget(e5_button(text="Snap",
                                        selected=True,
                                        colors=self.colors,
                                        call_back=self.take_photo))
                content_area.add_widget(bx)

            if gps_exists:
                bx = BoxLayout(orientation='vertical')
                if self.cfg.gps:
                    gps_label_text = 'Press start to begin.'
                elif self.ini.debug:
                    gps_label_text = 'Press start to begin [Debug mode].'
                else:
                    gps_label_text = 'No GPS available.'
                gps_label = e5_label(text=gps_label_text,
                                        id='gps_location')
                bx.add_widget(gps_label)
                bx.add_widget(e5_side_by_side_buttons(text=['Start', 'Stop', 'Clear'],
                                                        id=[''] * 3,
                                                        selected=[False] * 3,
                                                        call_back=[self.gps_manage] * 3,
                                                        colors=self.colors))
                self.gps_location_widget = gps_label
                content_area.add_widget(bx)

            if menu_exists:
                menu_list = ['True', 'False'] if self.cfg.current_field.inputtype == 'BOOLEAN' else self.cfg.current_field.menu

                if menu_filter:
                    menu_list = [menu for menu in menu_list if menu.upper()[0:len(menu_filter)] == menu_filter.upper()]

                selected_menu = self.cfg.get_field_data('')
                if not selected_menu and menu_list:
                    selected_menu = menu_list[0]

                if platform_name() == 'Android':
                    ncols = 1 if info_exists else 2
                else:
                    ncols = int(content_area.width / 400) if info_exists else int(content_area.width / 200)
                    ncols = max(ncols, 1)

                self.scroll_menu = e5_scrollview_menu(menu_list,
                                                           selected_menu,
                                                           widget_id='menu',
                                                           call_back=[self.menu_selection],
                                                           ncols=ncols,
                                                           colors=self.colors)
                content_area.add_widget(self.scroll_menu)

            if info_exists:
                content_area.add_widget(e5_scrollview_label(self.get_info(), colors=self.colors))

    def gps_manage(self, value):
        logger = logging.getLogger(__name__)
        if self.cfg.gps:
            if value.text == 'Start':
                logger.info('GPS started')
                gps.start()
                self.gps_location_widget.text = "Waiting for GPS."
            elif value.text == 'Stop':
                logger.info('GPS stopped')
                gps.stop()
                self.gps_location_widget.text = "GPS stopped."
            elif value.text == 'Clear':
                self.gps_location_widget.text = ''
        elif self.ini.debug:
            if value.text == 'Start':
                self.gps_location_widget.text = self.gps_random_point()
            elif value.text == 'Stop':
                pass
            elif value.text == 'Clear':
                self.gps_location_widget.text = ''

    def gps_random_point(self):
        point = "Bearing = %s\n" % round(random() * 360, 2)
        point += "Altitude = %s\n" % round(random() * 10, 3)
        point += "Lon = %s\n" % round(12.3912015 + random() / 10, 3)
        point += "Lat = %s\n" % round(51.3220704 + random() / 10, 3)
        point += "Speed = %s\n" % round(random() * 10, 3)
        point += "Accuracy = %s" % round(random() * 5 + 3, 3)
        return point

    def take_photo(self, instance):
        return
        if self.camera.play:
            try:
                self.camera.export_to_png(path.join(self.cfg.path, "IMG_%s.png" % self.datetime_stamp()))
            except Exception as e:
                print("Oops!", e.__class__, "occurred.")
                print('camera file save error')
                # TODO Replace this with a popup message
        self.camera.play = not self.camera.play

    def on_pre_enter(self):
        Window.bind(on_key_down=self._on_keyboard_down)
        if self.colors.need_redraw:
            pass

    def show_load_cfg(self):
        if self.cfg.filename and self.cfg.path:
            start_path = self.cfg.path
        else:
            start_path = self.ini.get_value(__program__, 'APP_PATH')
        if not path.exists(start_path):
            start_path = path.abspath(path.dirname(__file__))
        content = e5_LoadDialog(load=self.load,
                                cancel=self.dismiss_popup,
                                start_path=start_path,
                                button_color=self.colors.button_color,
                                button_background=self.colors.button_background)
        self.popup = Popup(title="Load CFG file", content=content,
                            size_hint=(0.9, 0.9))
        self.popup.open()

    def load(self, path, filename):
        self.dismiss_popup()
        self.load_cfg(filename[0])

    def update_mainscreen(self):
        self.mainscreen.clear_widgets()
        self.data_entry()

    def save_field(self):
        self.cfg.current_record[self.cfg.current_field.name] = self.field_data.textbox.text.replace('\n', '')
        self.field_data.textbox.text = ''

    def go_back(self, *args):
        if self.cfg.filename:
            self.save_field()
            self.cfg.previous()
            if self.cfg.BOF:
                self.cfg.filename = ''
                self.build_mainscreen()
            else:
                self.update_mainscreen()

    def go_next(self, *args):
        self.copy_from_menu_to_textbox()
        self.copy_from_gps_to_textbox()
        self.save_field()
        valid_data = self.cfg.data_is_valid(db=self.data.db.table(self.data.table))
        if valid_data is True:
            self.cfg.next()
            if self.cfg.EOF:
                self.save_record()
                self.cfg.start()
            self.update_mainscreen()
        else:
            widget = self.field_data.textbox
            widget.text = self.cfg.current_record[self.cfg.current_field.name]
            widget.focus = True
            self.popup = e5_MessageBox(self.cfg.current_field.name, valid_data, call_back=self.close_popup, colors=self.colors)
            self.popup.open()
            self.popup_open = True

    def menu_selection(self, value):
        self.field_data.textbox.text = value.text
        self.go_next(value)

    def exit_program(self):
        self.save_window_location()
        App.get_running_app().stop()

# region Edit Screens


class EditLastRecordScreen(e5_RecordEditScreen):
    pass


class EditPointsScreen(e5_DatagridScreen):
    pass


class EditCFGScreen(Screen):

    def __init__(self, e5_cfg=None, e5_ini=None, colors=None, **kwargs):
        super(EditCFGScreen, self).__init__(**kwargs)
        self.colors = colors if colors else ColorScheme()
        self.e5_ini = e5_ini
        self.e5_cfg = e5_cfg

    def on_pre_enter(self):
        # super(Screen, self).__init__(**kwargs)
        self.clear_widgets()

        layout = GridLayout(cols=1,
                            # id = 'fields',
                            size_hint_y=None
                            )
        layout.bind(minimum_height=layout.setter('height'))

        for field_name in self.e5_cfg.fields():
            f = self.e5_cfg.get(field_name)
            bx = GridLayout(cols=1, size_hint_y=None)
            bx.add_widget(e5_label("[" + f.name + "]", colors=self.colors))
            layout.add_widget(bx)

            bx = GridLayout(cols=2, size_hint_y=None)
            bx.add_widget(e5_label("Prompt", colors=self.colors))
            bx.add_widget(TextInput(text=f.prompt,
                                        multiline=False, size_hint_y=None))
            layout.add_widget(bx)

            bx = GridLayout(cols=2, size_hint_y=None)
            bx.add_widget(e5_label("Type", colors=self.colors))
            bx.add_widget(Spinner(text="Text", values=("Text", "Numeric", "Menu"),
                                        size_hint=(None, None),
                                        pos_hint={'center_x': .5, 'center_y': .5},
                                        color=self.colors.optionbutton_color,
                                        background_color=self.colors.optionbutton_background,
                                        background_normal=''))
            # self.StationMenu.size_hint  = (0.3, 0.2)
            layout.add_widget(bx)

            bx = GridLayout(cols=6, size_hint_y=None)

            bx.add_widget(e5_label("Carry", colors=self.colors))
            bx.add_widget(Switch(active=f.carry))

            bx.add_widget(e5_label("Unique", colors=self.colors))
            bx.add_widget(Switch(active=f.unique))

            bx.add_widget(e5_label("Increment", colors=self.colors))
            bx.add_widget(Switch(active=f.increment))

            layout.add_widget(bx)

            if f.inputtype == 'MENU':
                bx = GridLayout(cols=1, size_hint_y=None)
                button1 = e5_button(text='Edit Menu', size_hint_y=None,
                                    color=self.colors.optionbutton_color,
                                    background_color=self.colors.optionbutton_background,
                                    background_normal='',
                                    id=f.name)
                bx.add_widget(button1)
                button1.bind(on_press=self.show_menu)
                layout.add_widget(bx)

        root = ScrollView(size_hint=(1, .8))
        root.add_widget(layout)
        self.add_widget(root)

        buttons = GridLayout(cols=2, spacing=10, size_hint_y=None)

        button2 = e5_button(text='Back', size_hint_y=None,
                            color=self.colors.button_color,
                            background_color=self.colors.button_background,
                            background_normal='')
        buttons.add_widget(button2)
        button2.bind(on_press=self.go_back)

        button3 = e5_button(text='Save Changes', size_hint_y=None,
                            color=self.colors.button_color,
                            background_color=self.colors.button_background,
                            background_normal='')
        buttons.add_widget(button3)
        button3.bind(on_press=self.save)

        self.add_widget(buttons)

    def go_back(self, value):
        self.parent.current = 'MainScreen'

    def save(self, value):
        self.parent.current = 'MainScreen'

    def show_menu(self):
        pass


# ## End Edit Screens
# endregion

# region Help Screens
# ## Help Screens

class StatusScreen(e5_InfoScreen):

    def __init__(self, e5_data=None, e5_ini=None, e5_cfg=None, **kwargs):
        super(StatusScreen, self).__init__(**kwargs)
        self.e5_data = e5_data
        self.e5_ini = e5_ini
        self.e5_cfg = e5_cfg

    def on_pre_enter(self):
        txt = self.e5_data.status() if self.e5_data else 'A data file has not been initialized or opened.\n\n'
        txt += self.e5_cfg.status() if self.e5_cfg else 'A CFG is not open.\n\n'
        txt += self.e5_ini.status() if self.e5_ini else 'An INI file is not available.\n\n'
        txt += '\nThe default user path is %s.\n' % self.e5_ini.get_value(__program__, "APP_PATH")
        txt += '\nThe operating system is %s.\n' % platform_name()
        txt += '\nPython buid is %s.\n' % (python_version())
        txt += '\nLibraries installed include Kivy %s, TinyDB %s and Plyer %s.\n' % (__kivy_version__, __tinydb_version__, __plyer_version__)
        txt += '\nE5 was tested and distributed on Python 3.6, Kivy 1.10.1, TinyDB 3.11.1 and Plyer 1.4.0.\n'
        if self.e5_ini.debug:
            txt += '\nProgram is running in debug mode.\n'
        self.content.text = txt
        self.content.color = self.colors.text_color
        self.back_button.background_color = self.colors.button_background
        self.back_button.color = self.colors.button_color


class AboutScreen(e5_InfoScreen):
    def on_pre_enter(self):
        self.content.text = '\n\nE5 by Shannon P. McPherron\n\nVersion ' + __version__ + '\nCoconut Pie\n\n'
        self.content.text += 'Built on Python 3.8, Kivy 2.0.0, TinyDB 4.4.0 and Plyer 2.0.0\n\n'
        self.content.text += 'An OldStoneAge.Com Production\n\n' + __date__
        self.content.text += '\n\nSpecial thanks to Marcel Weiss,\n Jonathan Reeves and Li Li.\n\n'
        self.content.halign = 'center'
        self.content.valign = 'middle'
        self.content.color = self.colors.text_color
        self.back_button.background_color = self.colors.button_background
        self.back_button.color = self.colors.button_color

# ## End Help Screens
# endregion


sm = ScreenManager()


class E5App(App):

    def __init__(self, **kwargs):
        super(E5App, self).__init__(**kwargs)

        self.app_paths = AppDataPaths(APP_NAME)
        self.app_paths.setup()

    def build(self):
        sm.add_widget(MainScreen(name='MainScreen'))
        sm.current = 'MainScreen'
        self.title = __program__ + " " + __version__
        if 'exit' in sys.argv:
            self.stop()
        return sm


Factory.register(__program__, cls=E5App)


# From https://stackoverflow.com/questions/35952595/kivy-compiling-to-a-single-executable

def resourcePath():
    '''Returns path containing content - either locally or in pyinstaller tmp file'''
    if hasattr(sys, '_MEIPASS'):
        return path.join(sys._MEIPASS)

    return path.join(path.abspath("."))


if __name__ == '__main__':
    # This line goes with the function above
    resources.resource_add_path(resourcePath())  # add this line
    Config.set('input', 'mouse', 'mouse,multitouch_on_demand')      # Removes red dot
    Config.set('kivy', 'exit_on_escape', '0')
    E5App().run()
