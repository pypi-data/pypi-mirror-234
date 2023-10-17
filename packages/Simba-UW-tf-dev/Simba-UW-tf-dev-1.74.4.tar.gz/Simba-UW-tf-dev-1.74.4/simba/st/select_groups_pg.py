import streamlit as st
import pandas as pd
from st_aggrid import GridOptionsBuilder, AgGrid
from simba.mixins.config_reader import ConfigReader
from simba.utils.read_write import get_fn_ext


def get_cell_color(param):
    print(param.value)
    if param.value == 'TRUE':
        return {'color': 'white', 'backgroundColor': 'green'}
    else:
        return {'color': 'white', 'backgroundColor': 'red'}

class SelectGroupsPage():
    def __init__(self,
                 config: ConfigReader):

        self.videos = {}
        for video_path in config.machine_results_paths: self.videos[get_fn_ext(video_path)[1]] = video_path
        self.data_df = pd.DataFrame(data=list(self.videos.keys()), columns=['VIDEO'])
        self.group_cnt = st.selectbox(label='Number of groups', options=list(range(2, 11)), index=1)
        st.write("---")

        self.group_info = {}
        with st.container():
            print(self.group_cnt)
            for group_id in range(self.group_cnt):
                self.group_info[group_id+1] = {}
                self.group_info[group_id+1]['name'] = st.text_input(f'Group {group_id+1} name:', f'Group {group_id+1} Name')
        st.write("---")

        for group_id in self.group_info.keys():
            self.data_df[self.group_info[group_id]['name']] = 'FALSE'

        gb = GridOptionsBuilder.from_dataframe(self.data_df)
        for column in self.data_df.columns[1:]:
            gb.configure_column(column,
                                editable=True,
                                cellEditor='agSelectCellEditor',
                                cellEditorParams={'values': ['TRUE', 'FALSE']},
                                #cellStyle={'color': 'white', 'backgroundColor': 'green'}
                                )

        grid_options = gb.build()
        self.data_df = AgGrid(self.data_df, gridOptions=grid_options, allallow_unsafe_jscode=True)
        st.write("---")

        file_path = st.file_uploader("Import file")
        if file_path is not None:
            self.data_df = pd.read_csv(file_path)
            st.info('Group data loaded.')