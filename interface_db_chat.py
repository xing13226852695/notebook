import time
import pandas as pd
from pandasai import SmartDataframe
from pandasai.llm.openai import OpenAI
import streamlit as st
from impala.dbapi import connect
from PIL import Image

llm = OpenAI(
    api_token="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",
    temperature=0,
    seed=26,
)

conn = connect(
    host="192.168.2.3",
    port="10000",
    user="root",
    password="Bigdata_2022",
    database="openai",
    auth_mechanism="PLAIN",
)


def query_agent(query):
    """
    Query an agent and return the response as a string.

    Args:
        agent: The agent to query.
        query: The query to ask the agent.

    Returns:
        The response from the agent as a string.
    """

    prompt = """""" + query

    # Run the prompt through the agent
    return prompt.__str__()


def create_agent():
    """
    Create an agent that can access and use a large language model (LLM).

    Args:
        filename: The path to the CSV file that contains the data.

    Returns:
        An agent that can access and use the LLM.
    """

    # SQL查询
    query_sql = "SELECT * FROM paper_tech_measure_synthetic"

    # 从查询结果中创建DataFrame
    df_1 = pd.read_sql_query(query_sql, conn)

    df_2 = SmartDataframe(
        df_1, config={"llm": llm, "custom_whitelisted_dependencies": ["networkx"]}
    )

    return df_2


st.title("👨‍💻 Chat with your Database")

query = st.text_area("Insert your query")

if st.button("Submit Query", type="primary"):
    response = query_agent(query=query)
    df = create_agent()
    answer = df.chat(response)
    print(answer)
    time.sleep(10)
    image = Image.open("C:/Users/xwp19/exports/charts/temp_chart.png")
    st.image(image, caption="Result display")
