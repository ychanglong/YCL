import cx_Oracle
import pandas as pd
import config
import os
import logging.config
import yaml
from styleframe import StyleFrame, Styler, utils
from pretty_html_table import build_table
from send_email import send_mail


logging.config.dictConfig(yaml.safe_load(open("config.yaml")))
logger = logging.getLogger("file")


def connectToOracle(dsn_tns, username, password):
    connection = cx_Oracle.connect(user=username, password=password, dsn=dsn_tns)
    return connection


def get_df(dsn_tns):
    try:
        c = connectToOracle(dsn_tns, config.username, config.password)
        df = pd.read_sql(config.stmt, con=c)
        return df
    except cx_Oracle.DatabaseError as ex:
        err, = ex.args
        logger.error("Error code = ", err.code)
        logger.error("Error Message = ", err.message)
        os._exit(1)
    c.close()


def customize_df(df1, df2, attachment):
    excel_writer = StyleFrame.ExcelWriter(attachment)

    sf1 = StyleFrame(df1)
    sf1.apply_style_by_indexes(
        indexes_to_style=sf1[~sf1['SMT Critical Incidents'].str.contains('Date')],
        cols_to_style=list(df1.columns),
        styler_obj=Styler(
            font="Arial",
            font_size=10,
            border_type=None,
            shrink_to_fit=True,
            horizontal_alignment="left",
        ),
    )

    sf1.apply_style_by_indexes(
        indexes_to_style=sf1[sf1['SMT Critical Incidents'].str.contains('Date')],
        cols_to_style=list(df1.columns),
        styler_obj=Styler(
            font="Arial",
            font_size=9,
            font_color="white",
            bg_color="#0b64a0",
            shrink_to_fit=True,
            horizontal_alignment="left",
        ),
    )

    sf1.apply_headers_style(
        Styler(
            font="Arial",
            font_size=16,
            border_type=None,
            wrap_text=False,
            shrink_to_fit=True,
            underline="single",
            horizontal_alignment="left",
        )
    )

    sf2 = StyleFrame(df2)
    sf2.apply_column_style(
        cols_to_style=list(df2.columns),
        styler_obj=Styler(
            font="Arial",
            font_size=9,
            wrap_text=True,
            horizontal_alignment="left",
            vertical_alignment="center",
        ),
        style_header=False,
    )
    sf2.apply_headers_style(
        Styler(
            font="Arial",
            font_size=9,
            font_color="white",
            wrap_text=True,
            bg_color="#0b64a0",
            bold=True,
            horizontal_alignment="left",
            vertical_alignment="center",
        )
    )

    sf1.to_excel(excel_writer=excel_writer, best_fit=list(df1.columns), startrow=1)
    sf2.to_excel(excel_writer=excel_writer, best_fit=list(df2.columns), startrow=10)
    excel_writer.save()


def reminder_cto(df):
    subject = "Quality check"
    start = """<html>
                <body>
                    <p style="font-family:Arial;font-size:13px">Hello team,<br><br>
                    Please be aware of below incident ticket(s), problem ticket is not created.</br></br></p>"""
    content = build_table(df, "blue_light", font_size="13px", font_family="Arial")
    end = """</body>
        </html>
        """
    body = start + content + end
    # sender = "CI-Service-Center-Suzhou@cn.bosch.com"
    sender =  "jared.ma@cn.bosch.com"
    # recipient = "Global-Critical-Ticket-Ownership@bcn.bosch.com"
    recipient= "jared.ma@cn.bosch.com"
    send_mail(subject, sender, recipient, body)


if __name__ == "__main__":
    dsn_tns = cx_Oracle.makedsn(
        config.hostname, config.port, service_name=config.service_name
    )
    logger.info("Getting data from oracle database...")
    df = get_df(dsn_tns)
    df["Down Time (hhh:mi)"].fillna(value="Not specified", inplace=True)
    if not df.empty:
        logger.info("Generating report...")
        customize_df(config.df_summary, df, config.attachment)
        logger.info("Sending email...")
        send_mail(
            config.subject,
            config.sender,
            config.recipient,
            config.body,
            attachment=config.attachment,
        )
        # delete today's incident ticket
        for index, row in df.iterrows():
            if pd.Timestamp(row["Created Date(UTC+0)"], tz=None).date() == config.today:
                df.drop(index, inplace=True)
        # filter for quality check which PBI is empty
        filt_null = pd.isnull(df["Related Problem ID"])
        filt_status = (df['STATUS'] == 'Resolved')
        new_df = df.loc[filt_null & filt_status, ("Incident ID", "Assigned Group")]
        if not new_df.empty and config.now.strftime("%H") == "13":
            reminder_cto(new_df)
            logger.info("Quality check email is sent successfully!")
    else:
        logger.info("No critical tickets found, sending email...")
        send_mail(config.subject, config.sender, config.recipient, config.body_no_results)

    logger.info("Email is sent successfully!")

