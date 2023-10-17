import streamlit as st
from streamlit_option_menu import option_menu
import os

from enums import SIDEBAR_OPTIONS
import simba
from simba.mixins.config_reader import ConfigReader
from select_groups_pg import SelectGroupsPage
from aggregate_statistics import AggregateStatistics
from welcome_page import WelcomePage


class StreamlitApp():
    def __init__(self,
                 config_path='/Users/simon/Desktop/envs/troubleshooting/two_black_animals_14bp/project_folder/project_config.ini'):

        self.config = ConfigReader(config_path=config_path)
        self.simba_dir = os.path.dirname(simba.__file__)
        self.favicon_path = os.path.join(self.simba_dir, 'assets/icons/simba/SimBA_logo.ico')
        st.set_page_config(page_title='SimBA', page_icon=self.favicon_path)

    def run(self):
        with st.sidebar:
            sidebar_selection = option_menu(menu_title=None, options=SIDEBAR_OPTIONS.list(), default_index=0)
        st.title(sidebar_selection)
        if sidebar_selection == SIDEBAR_OPTIONS.WELCOME.value:
            project_data = WelcomePage(config=self.config)
        if sidebar_selection == SIDEBAR_OPTIONS.DEFINE_GROUPS.value:
            SelectGroupsPage(config=self.config)
        if sidebar_selection == SIDEBAR_OPTIONS.AGGREGATE_STATISTICS.value:
            AggregateStatistics(config=self.config)

if __name__ == '__main__':
    app = StreamlitApp()
    app.run()





    #if sidebar_selection == SIDEBAR_OPTIONS.DEFINE_GROUPS.value:






