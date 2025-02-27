import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from ConvexHull.jarvisMarch import JarvisMarch
from ConvexHull.grhamScan import GrahamScan
from ConvexHull.quickHull import QuickHull
from ConvexHull.bruteForce import BruteForce

from LineIntersection.lineIntersection import LineIntersection


def plot_graph(x, y):
    fig, ax = plt.subplots()
    ax.scatter(x, y, color="blue")
    st.pyplot(fig)


algo = "Jarvis March"


def convex_hull_page():
    st.empty()
    header_text = "Convex Hull Visualizer"
    st.markdown(
        f"""
    <h1 style='text-align: center; color: #40916c;'>{header_text}</h1>
    """,
        unsafe_allow_html=True,
    )
    option = st.selectbox(
        "Choose an option:",
        ("Enter Points Individually", "Generate Random Points", "Add Points from CSV"),
    )

    if "x_points" not in st.session_state:
        st.session_state.x_points = []
    if "y_points" not in st.session_state:
        st.session_state.y_points = []

    if option == "Enter Points Individually":
        header_text = "Enter Points Individually"
        st.markdown(
            f"""
        <h3 style='text-align: center; color: #95d5b2;'>{header_text}</h3>
        """,
            unsafe_allow_html=True,
        )
        input_col, table_col = st.columns(2)

        with input_col:
            header_text = "Enter Coordinates"
            st.markdown(
                f"""
            <h4 style='text-align: center; color: #d8f3dc;'>{header_text}</h4>
            """,
                unsafe_allow_html=True,
            )
            x_input = st.text_input("Enter X coordinate:")
            y_input = st.text_input("Enter Y coordinate:")

            point_col, clear_col = st.columns(2)
            with point_col:
                if st.button("Add Point"):
                    try:
                        x = float(x_input) if x_input else 0.0
                        y = float(y_input) if y_input else 0.0
                        st.session_state.x_points.append(x)
                        st.session_state.y_points.append(y)
                        st.success(f"Point ({x}, {y}) added.")
                    except ValueError:
                        st.error(
                            "Invalid input. Please enter valid numerical values for X and Y coordinates."
                        )

            with clear_col:
                if st.button("Clear Points"):
                    st.session_state.x_points = []
                    st.session_state.y_points = []
                    st.success("Points cleared.")

        with table_col:
            points_df = pd.DataFrame(
                list(zip(st.session_state.x_points, st.session_state.y_points)),
                columns=["X", "Y"],
            )
            header_text = "Points Added"
            st.markdown(
                f"""
            <h4 style='text-align: center; color: #d8f3dc;'>{header_text}</h4>
            """,
                unsafe_allow_html=True,
            )
            st.dataframe(points_df, height=200, width=800)

    elif option == "Generate Random Points":
        header_text = "Generate Random Points"
        st.markdown(
            f"""
        <h3 style='text-align: center; color: #95d5b2;'>{header_text}</h3>
        """,
            unsafe_allow_html=True,
        )
        point_col, table_col = st.columns(2)
        with point_col:
            st.subheader("Min/Max Point")
            num_points = st.number_input(
                "Enter the number of points:", min_value=1, value=5, step=1
            )
            min_range = st.number_input("Enter minimum value:", value=0)
            max_range = st.number_input("Enter maximum value:", value=10)
            if st.button("Generate Points"):
                st.session_state.x_points = np.random.uniform(
                    min_range, max_range, num_points
                ).tolist()
                st.session_state.y_points = np.random.uniform(
                    min_range, max_range, num_points
                ).tolist()

        with table_col:
            points_df = pd.DataFrame(
                list(zip(st.session_state.x_points, st.session_state.y_points)),
                columns=["X", "Y"],
            )

            header_text = "Added Points"
            st.markdown(
                f"""
            <h4 style='text-align: center; color: #d8f3dc;'>{header_text}</h4>
            """,
                unsafe_allow_html=True,
            )
            st.dataframe(points_df, height=200, width=800)

    elif option == "Add Points from CSV":
        header_text = "Add Points from CSV"
        st.markdown(
            f"""
        <h3 style='text-align: center; color: #95d5b2;'>{header_text}</h3>
        """,
            unsafe_allow_html=True,
        )
        point_col, table_col = st.columns(2)
        with point_col:
            st.subheader("Upload CSV file")
            uploaded_file = st.file_uploader("CSV", type=["csv"])
            if uploaded_file is not None:
                df = pd.read_csv(uploaded_file)
                st.session_state.x_points = df.get("x", [])
                st.session_state.y_points = df.get("y", [])

        with table_col:
            points_df = pd.DataFrame(
                list(zip(st.session_state.x_points, st.session_state.y_points)),
                columns=["X", "Y"],
            )

            header_text = "Added Points"
            st.markdown(
                f"""
            <h4 style='text-align: center; color: #d8f3dc;'>{header_text}</h4>
            """,
                unsafe_allow_html=True,
            )
            st.dataframe(points_df, height=200, width=800)

    header_text = "Convex Hull"
    st.markdown(
        f"""
    <h3 style='text-align: center; color: #95d5b2;'>{header_text}</h3>
    """,
        unsafe_allow_html=True,
    )
    draw_convex_hull()


def draw_convex_hull():
    points = np.column_stack((st.session_state.x_points, st.session_state.y_points))
    algo = st.selectbox(
        "Choose an algorithm:",
        ("Jarvis March", "Graham Scan", "QuickHull", "Brute Force"),
    )

    if algo == "Jarvis March":
        jm = JarvisMarch(points=points)
        hull_points = jm()
        # fig = jm.plot_step_by_step()
        fig = jm.create_animation()
        st.plotly_chart(fig, use_container_width=True)

    elif algo == "Graham Scan":
        gs = GrahamScan(points=points)
        hull_points = gs()
        fig = gs.plot_step_by_step()
        st.plotly_chart(fig, use_container_width=True)
    elif algo == "QuickHull":
        qh =JarvisMarch(points=points)
        hull_points = qh()
        fig = qh.plot_step_by_step()
        st.plotly_chart(fig, use_container_width=True)
    elif algo == "Brute Force":
        bf = BruteForce(points=points)
        hull_points = bf()
        fig = bf.create_animation()
        st.plotly_chart(fig, use_container_width=True)
        pass
    else:
        pass

    if hull_points is not None:
        header_text = "Convex Hull Points"
        st.markdown(
            f"""
        <h3 style='text-align: center; color: #95d5b2;'>{header_text}</h3>
        """,
            unsafe_allow_html=True,
        )
        st.dataframe(hull_points, height=200, width=800, hide_index=True)


def line_intersection_page():
    st.empty()
    header_text = "Line Intersection Visualizer"
    st.markdown(
        f"""
        <h1 style='text-align: center; color: #40916c'>{header_text}</h1>
        """,
        unsafe_allow_html=True,
    )
    option = st.selectbox(
        "Choose an option:",
        ("Enter Points Individually", "Generate Random Points", "Add Points from CSV"),
    )

    if "line_1" not in st.session_state:
        st.session_state.line_1 = []
    if "line_2" not in st.session_state:
        st.session_state.line_2 = []

    if option == "Enter Points Individually":
        header_text = "Enter Points Individually"
        st.markdown(
            f"""
        <h3 style='text-align: center; color: #95d5b2;'>{header_text}</h3>
        """,
            unsafe_allow_html=True,
        )
        input_col, table_col = st.columns(2)

        with input_col:
            header_text = "Enter Coordinates"
            st.markdown(
                f"""
            <h4 style='text-align: center; color: #d8f3dc;'>{header_text}</h4>
            """,
                unsafe_allow_html=True,
            )
            x_input = st.text_input("Enter X coordinate:")
            y_input = st.text_input("Enter Y coordinate:")

            point_col, clear_col = st.columns(2)
            with point_col:
                if st.button("Add Point"):
                    try:
                        x = float(x_input) if x_input else 0.0
                        y = float(y_input) if y_input else 0.0
                        if (
                            len(st.session_state.line_1) > 4
                            or len(st.session_state.line_2) > 4
                        ):
                            st.error(
                                "Only 4 points can be added, Please clear the points first."
                            )
                        st.session_state.line_1.append(x)
                        st.session_state.line_2.append(y)
                        st.success(f"Point ({x}, {y}) added.")
                    except ValueError:
                        st.error(
                            "Invalid input. Please enter valid numerical values for X and Y coordinates."
                        )

            with clear_col:
                if st.button("Clear Points"):
                    st.session_state.line_1 = []
                    st.session_state.line_2 = []
                    st.success("Points cleared.")

        with table_col:
            points_df = pd.DataFrame(
                list(zip(st.session_state.line_1, st.session_state.line_2)),
                columns=["X", "Y"],
            )
            header_text = "Added Points"
            st.markdown(
                f"""
            <h4 style='text-align: center; color: #d8f3dc;'>{header_text}</h4>
            """,
                unsafe_allow_html=True,
            )
            st.table(points_df)

    elif option == "Generate Random Points":
        header_text = "Generate Random Points"
        st.markdown(
            f"""
        <h3 style='text-align: center; color: #95d5b2;'>{header_text}</h3>
        """,
            unsafe_allow_html=True,
        )
        point_col, table_col = st.columns(2)
        with point_col:
            st.subheader("Min/Max Point")
            min_range = st.number_input("Enter minimum value:", value=0)
            max_range = st.number_input("Enter maximum value:", value=10)
            if st.button("Generate Points"):
                line_1 = np.random.uniform(min_range, max_range, 4)
                line_2 = np.random.uniform(min_range, max_range, 4)
                st.session_state.line_1 = line_1.tolist()
                st.session_state.line_2 = line_2.tolist()

        with table_col:
            points_df = pd.DataFrame(
                list(zip(st.session_state.line_1, st.session_state.line_2)),
                columns=["X", "Y"],
            )

            header_text = "Added Points"
            st.markdown(
                f"""
            <h4 style='text-align: center; color: #d8f3dc;'>{header_text}</h4>
            """,
                unsafe_allow_html=True,
            )
            st.table(points_df)

    elif option == "Add Points from CSV":
        header_text = "Add Points from CSV"
        st.markdown(
            f"""
        <h3 style='text-align: center; color: #95d5b2;'>{header_text}</h3>
        """,
            unsafe_allow_html=True,
        )
        point_col, table_col = st.columns(2)
        with point_col:
            st.subheader("Upload CSV file")
            uploaded_file = st.file_uploader("CSV", type=["csv"])
            if uploaded_file is not None:
                df = pd.read_csv(uploaded_file)
                if len(df.columns) != 2 or len(df.index) < 4:
                    st.error("Invalid CSV file. Please upload a valid CSV file.")
                if len(df.index) > 4:
                    df = df.head(4)
                    st.info("Size too large, only first 4 rows are considered.")
                st.session_state.line_1 = df.get("x", [])
                st.session_state.line_2 = df.get("y", [])

        with table_col:
            points_df = pd.DataFrame(
                list(zip(st.session_state.line_1, st.session_state.line_1)),
                columns=["X", "Y"],
            )

            header_text = "Added Points"
            st.markdown(
                f"""
            <h4 style='text-align: center; color: #d8f3dc;'>{header_text}</h4>
            """,
                unsafe_allow_html=True,
            )
            st.table(points_df)

    header_text = "Intersection"
    st.markdown(
        f"""
    <h3 style='text-align: center; color: #95d5b2;'>{header_text}</h3>
    """,
        unsafe_allow_html=True,
    )
    if len(st.session_state.line_1) == 4:
        draw_intersection_points()
    else:
        st.info("Please add 4 points to find intersection points.")


def draw_intersection_points():
    algo = st.selectbox(
        "Choose an algorithm:",
        ("Brute Force", "Sweep Line", "One More (TBD)"),
    )
    lines = [
        item
        for pair in zip(st.session_state.line_1, st.session_state.line_2)
        for item in pair
    ]
    line1 = lines[: len(lines) // 2]
    line2 = lines[len(lines) // 2 :]
    if algo == "Brute Force":
        bf = LineIntersection(line1=line1, line2=line2)
        intersect_points = bf()
        fig = bf.plot_step_by_step()
        st.plotly_chart(fig, use_container_width=True)

    elif algo == "Sweep Line":
        bf = LineIntersection(line1=line1, line2=line2)
        intersect_points = bf()
        fig = bf.plot_step_by_step()
        st.plotly_chart(fig, use_container_width=True)
    else:
        pass


def report_page():
    st.empty()
    header_text = "Design and Analysis of Geometric Algorithms"
    st.markdown(
        f"""
        <h1 style='text-align: center; color: #40916c'>{header_text}</h1>
        """,
        unsafe_allow_html=True,
    )

    with open("./templates/credits.html", "r") as file:
        html_content = file.read()

    st.markdown(html_content, unsafe_allow_html=True)

    with open("./templates/report.html", "r") as f:
        html_string = f.read()
    st.markdown(
        html_string,
        unsafe_allow_html=True,
    )
    st.subheader("All rights reserved by Ashad (and only Ashad).")


def main():
    st.sidebar.title("Geometry Overpowerred")
    choice = st.sidebar.radio(
        "Menu:",
        ("Report", "Convex Hull Algorithms", "Line Intersection Algorithms"),
    )

    if choice == "Report":
        report_page()
    elif choice == "Convex Hull Algorithms":
        convex_hull_page()
    elif choice == "Line Intersection Algorithms":
        line_intersection_page()


if __name__ == "__main__":
    main()
