import streamlit as st
import pandas as pd
import altair as alt
from simba.mixins.config_reader import ConfigReader
from simba.mixins.train_model_mixin import TrainModelMixin

class AggregateStatistics():
    def __init__(self,
                 config: ConfigReader):

        col_1, col_2 = st.columns(2)
        self.config, self.data = config, None
        self.select_clf = col_1.selectbox(label='', options=config.clf_names, on_change=None)
        self.select_agg = col_2.selectbox(label='', options=['VIDEO', 'GROUP'], on_change=None)
        st.button("RUN", on_click=lambda: self.run())
        st.write("---")

    @staticmethod
    @st.experimental_memo
    def read_data(_config: ConfigReader) -> pd.DataFrame:
        return TrainModelMixin().read_all_files_in_folder_mp(file_paths=_config.machine_results_paths,
                                                             file_type=_config.file_type,
                                                             classifier_names=_config.clf_names)

    @staticmethod
    @st.experimental_memo
    def video_aggregator(df: pd.DataFrame, video_info: pd.DataFrame, clf: str) -> pd.DataFrame:
        df = df.groupby('VIDEO')[clf].agg(['sum', 'count']).rename(columns={'sum': 'clf_frame_count', 'count': 'video_frame_count'})
        df['fps'] = df.index
        df['fps'] = df['fps'].map(video_info[['Video', 'fps']].set_index('Video').squeeze().to_dict())
        df[f'{clf} (seconds)'] = round(df['clf_frame_count'] / df['fps'], 3)
        df[f'{clf} (% session)'] = round(df['clf_frame_count'] / df['video_frame_count'], 3)

        return df.reset_index()

    def group_aggregator(df: pd.DataFrame, video_info: pd.DataFrame, clf: str, group_df: pd.DataFrame) -> pd.DataFrame:
        pass

    def run(self):
        data = self.read_data(_config=self.config).reset_index().rename(columns={'index': 'VIDEO'})
        if self.select_agg == 'VIDEO':
            df = self.video_aggregator(df=data, video_info=self.config.video_info_df, clf=self.select_clf)
            chart = (alt.Chart(df).mark_bar().encode(alt.X("VIDEO"), alt.Y(f"{self.select_clf} (seconds)"), alt.Color("VIDEO"), alt.Tooltip("VIDEO")).interactive())
        if self.select_agg == 'VIDEO':
            pass


        st.altair_chart(chart, use_container_width=True)
        st.write("---")