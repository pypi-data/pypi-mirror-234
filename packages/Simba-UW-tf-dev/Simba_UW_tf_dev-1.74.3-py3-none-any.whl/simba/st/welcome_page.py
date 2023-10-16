import streamlit as st
from simba.mixins.config_reader import ConfigReader
from simba.mixins.train_model_mixin import TrainModelMixin


class WelcomePage():
    def __init__(self,
                 config: ConfigReader):
        st.info('HELLO!')



