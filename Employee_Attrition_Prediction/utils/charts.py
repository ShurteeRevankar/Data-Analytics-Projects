import plotly.express as px
import plotly.graph_objects as go


# ----------------------------
# Gender Distribution
# ----------------------------
def gender_distribution(df):
    fig = px.pie(
        df,
        names="Gender",
        title="Gender Distribution",
        hole=0.45
    )

    fig.update_traces(textposition="inside", textinfo="percent+label")

    fig.update_layout(
        template="plotly_white",
        height=450
    )

    return fig


# ----------------------------
# Department Distribution
# ----------------------------
def department_distribution(df):
    dept = (
        df["Department"]
        .value_counts()
        .reset_index()
    )

    dept.columns = ["Department", "Employees"]

    fig = px.bar(
        dept,
        x="Department",
        y="Employees",
        color="Department",
        text="Employees",
        title="Employees by Department"
    )

    fig.update_layout(
        template="plotly_white",
        showlegend=False,
        height=450
    )

    return fig


# ----------------------------
# Job Role Distribution
# ----------------------------
def job_role_distribution(df):
    roles = (
        df["JobRole"]
        .value_counts()
        .reset_index()
    )

    roles.columns = ["JobRole", "Employees"]

    fig = px.bar(
        roles,
        x="Employees",
        y="JobRole",
        orientation="h",
        color="Employees",
        title="Employees by Job Role"
    )

    fig.update_layout(
        template="plotly_white",
        height=500,
        yaxis={"categoryorder": "total ascending"}
    )

    return fig


# ----------------------------
# Attrition by Department
# ----------------------------
def attrition_department(df):

    temp = (
        df.groupby(["Department", "Attrition"])
        .size()
        .reset_index(name="Count")
    )

    fig = px.bar(
        temp,
        x="Department",
        y="Count",
        color="Attrition",
        barmode="group",
        title="Attrition by Department"
    )

    fig.update_layout(
        template="plotly_white",
        height=450
    )

    return fig


# ----------------------------
# Attrition by Overtime
# ----------------------------
def overtime_attrition(df):

    temp = (
        df.groupby(["OverTime", "Attrition"])
        .size()
        .reset_index(name="Count")
    )

    fig = px.bar(
        temp,
        x="OverTime",
        y="Count",
        color="Attrition",
        barmode="group",
        title="Attrition vs Overtime"
    )

    fig.update_layout(
        template="plotly_white",
        height=450
    )

    return fig


# ----------------------------
# Monthly Income Distribution
# ----------------------------
def income_distribution(df):

    fig = px.histogram(
        df,
        x="MonthlyIncome",
        nbins=30,
        title="Monthly Income Distribution"
    )

    fig.update_layout(
        template="plotly_white",
        height=450
    )

    return fig


# ----------------------------
# Salary by Department
# ----------------------------
def salary_department(df):

    fig = px.box(
        df,
        x="Department",
        y="MonthlyIncome",
        color="Department",
        title="Salary Distribution by Department"
    )

    fig.update_layout(
        template="plotly_white",
        showlegend=False,
        height=450
    )

    return fig


# ----------------------------
# Age Distribution
# ----------------------------
def age_distribution(df):

    fig = px.histogram(
        df,
        x="Age",
        nbins=20,
        title="Age Distribution"
    )

    fig.update_layout(
        template="plotly_white",
        height=450
    )

    return fig


# ----------------------------
# Performance Rating
# ----------------------------
def performance_rating(df):

    fig = px.histogram(
        df,
        x="PerformanceRating",
        color="PerformanceRating",
        title="Performance Rating Distribution"
    )

    fig.update_layout(
        template="plotly_white",
        showlegend=False,
        height=450
    )

    return fig


# ----------------------------
# Correlation Heatmap
# ----------------------------
def correlation_heatmap(df):

    numeric = df.select_dtypes(include="number")

    corr = numeric.corr()

    fig = go.Figure(
        data=go.Heatmap(
            z=corr.values,
            x=corr.columns,
            y=corr.columns,
            colorscale="RdBu",
            zmin=-1,
            zmax=1,
            text=corr.round(2),
            texttemplate="%{text}"
        )
    )

    fig.update_layout(
        title="Correlation Heatmap",
        template="plotly_white",
        height=700
    )

    return fig