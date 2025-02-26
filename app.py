from web_process import news_result
from pdf_process import answer_question_from_pdf
import streamlit as st

st.set_page_config(page_title="AInquire", layout="wide")

data_dict = {"model": None, "api_key": None, "target": None, "question": None, "result": None}
if "data" not in st.session_state:
    st.session_state.data = data_dict

url_tab, pdf_tab = st.tabs(["URL", "PDF"])

with st.sidebar:
    with st.popover("Select OpenAI Model"):
        model = st.selectbox("Select OpenAI Model", ["gpt-4o", "gpt-4-turbo", "gpt-4", "gpt-3.5-turbo", "gpt-3.5-turbo-0125", "other"])
        other_model = st.empty()
        if model == "other":
            other_model = other_model.text_input("Write OpenAI Model")
            model = other_model
            del other_model
        else:
            other_model.empty()
        api_key = st.text_input("API Key", type="password", key="api_key")
        data_dict.update({"model": model, "api_key": api_key})
        del model, api_key

    st.divider()
    st.write(f"Model : {data_dict['model']}")
    st.write(f"API Key : {data_dict['api_key'][:5] + len(data_dict['api_key'][5:]) * '*'}")


def form(target_type):
    global data_dict

    control_dict = {"URL": news_result, "PDF": answer_question_from_pdf}
    url_col1, url_col2 = st.columns(2)

    with url_col1:
        st.empty()
        if target_type == "URL":
            target_widget = st.text_input("Web URL", key="target_widget_url")
        else:
            target_widget = st.file_uploader("PDF dosyasını yükle", type="pdf", key="target_widget_pdf")
        question = st.text_area("Your Question", key=f"question_{target_type}")
        button_key = f"button_{target_type}"

        if st.button("Answer!", type="primary", key=button_key):
            data_dict["result"] = None
            data_dict.update({"target": target_widget, "question": question})
            del target_widget, question
            st.session_state.data = data_dict

            target_function = control_dict.get(target_type)
            if target_function:
                st.session_state.data["result"] = target_function(st.session_state.data)

    with url_col2:
        st.empty()
        if st.session_state.data["result"] is not None:
            st.text_area("Result", st.session_state.data["result"], height=500, disabled=True, label_visibility="hidden", key=f"result_{target_type}")
            data_dict = {"model": None, "api_key": None, "target": None, "question": None, "result": None}
            st.session_state.data = data_dict


with url_tab:
    form("URL")


with pdf_tab:
    form("PDF")
