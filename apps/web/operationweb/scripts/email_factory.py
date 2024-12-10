
# Use HTML format to edit Email message
# Define Email templates for Email service


def get_email_msg(host_name, host_used_by, email_type, incident=''):

    # Define Email message
    email_msg = {}

    # Disk:C full
    if email_type == '1':
        if incident:
            email_msg['subject'] = '[' + str(incident) + '] Disk C cleanup for server ' + host_name
        else:
            email_msg['subject'] = 'Disk C cleanup for server ' + host_name
        email_msg['content'] = '''
            <!DOCTYPE html>
            <html lang="en">
                <head>
                    <title>Disk C Usage Reached 99%</title>
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
                    <meta name="color-scheme" content="only">
                    <meta http-equiv="X-Render-Mode" content="html">
                    <style type="text/css">
                        body {{font-size: 16px; line-height: 24px; font-family: Bosch Office Sans, Arial, sans-serif;}}
    
                        a {{text-decoration: none; color: #007BC0;}}
    
                        @media screen and (max-width: 640px) {{
                            #innerTable {{width: 320px !important;}}
    
                            #header-logo {{
                                display: block !important;
                                float: left !important;
                                width: 100% !important;
                            }}
    
                            #header-text {{
                                display: block !important;
                                float: left !important;
                                width: 100% !important;
                                text-align: left !important;
                                padding: 0px 0px 0px 16px !important;
                            }}
    
                            .dyn-col {{
                                display: block !important;
                                float: left !important;
                                width: 100% !important;
                                box-sizing: border-box !important;
                            }}
                        }}
    
                        @supports (-webkit-touch-callout: none) {{
                            body {{
                                background-color: #EFF1F2;
                            }}
                        }}
                    </style>
                </head>
    
                <body style="margin: 0px;">
                    <table id="outerTable" cellpadding="0" cellspacing="0" border="0" style="width: 100%; background-color: #EFF1F2;">
                        <tr>
                            <td>
                                <span
                                    style="color: #EFF1F2; display: none; opacity: 0; overflow: hidden; mso-hide: all; visibility: hidden;">
                                    Customer Notification - Disk C Usage Reached 99%<br>
                                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                                </span>
    
                                <table id="innerTable" cellpadding="0" cellspacing="0" border="0" align="center" style="width: 640px; background-color: #FFF; margin-bottom: 16px;">
                                    <tr>
                                        <td colspan="2" style="line-height: 0px;">
                                            <img width="640" height="6" style="height: 6px; width: 100%;" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAABQAAAAAMCAMAAAAKwOAZAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAADwUExURZUkMp8kNLEnOa8gJMEhKtQgJ54vZn42hW03jWo4jWg4jmU5jmM5jmE6jl86jlw7jlk7j1c8j1M8j1A9j00+kEo+kEk/kEc/kEY/kERAkEJAkD9BkTxBkTo8gDc8gDU8fzM8fy89fiw9fSk9fSU+gyY8gig7gCo4hiNAhiVdoSZeoi9+tTmUwDijyzmjyzqkywWmywWetgqdXAqdXQqcXkGoZIm8blOuamKxbTKNRrAkMbIpTiM+hBClygWlywablB6iYjmfWzB+th2lyXu5bDKWULAiKy6kxweac2+2a4o1fQWlyidOljGNRjB/tgAAAJPcmuEAAABQdFJOU/////////////////////////////////////////////////////////////////////////////////////////////////////////8AE3OmeQAAAAlwSFlzAAAOwwAADsMBx2+oZAAABWBJREFUaEPd221v2lYYxvEpoQ30DXkZpIBIkICmhRCUjIx02bRm0oqWfv+Ps/vhOk9gE/v42HX3Pwfbadq3P9226S8NtD3pbKM+286p7V2ben929oGSw0Hn2LKwM7twGwt7r0HQ5aVuNBrOxmP+6D5o6q/DZvPcNa2y3m52vPnHFH2q1qKxVjV0t26oh18T9/BtQ+vhtwaCUXW2PYlvC/5OTzuwpxWdkHNZBLJ5WfxlKMjg2Y0VbC9x72JEH1qhf5eD2dA0HgI9L0+/8fRqcqV74pp/mWSv+RdpGrcKMAjp8gJh1QJksX0HT/X3O9BK2R/wKbL7oq3/hFvJ2jxSm79hVK0BqVoDZjG1FMB36l3mBOj4c0uyBCp79iKDQM4zkPzDGDgjAEMCB06/HAGvXEyfbjRl5ua85hO68D+kGJ2nymAMhHw4xiCgywuEVeuvan0GT7V32yIAwVqJ1nArWS8M4OP/BsCn+BmwpQA+feieCX/mozF2IiAMtOOffPZi8HTbhW1OtkviT6Y/NlDs80bAsS/gQVPQJzF9ukzWNxuRyCryL2gI5J+w5JellzKYGaDL698bIFalT5AssooA3hZvsVo9J271D0Qr1L2uqNbfAFeyeATcgKh6g1G1to0G0PnXroeA+ggwMyUwWLydgcqeHtw1FvZ+gxEryA6qfnn+ZRgI+6QD/zIA1GgEVLz4yv6Av21wK7R00zqYBAFdTvMU/v04AOFa4b5CrZSBtiLdyyG29A8BGcBGHgG2/BlgSwHs7GT+0yGQM2c7/Kl8OvvZ6c9eUI4/NU9O5hLbphPgTMbA/QnQAGj1CwkMJ0Ci75qWJ6CSlhP7J1OgEigbCJZhMDi5IF1OSQbAqrfA0KxMAK1sy+QD4HPhdyCsHyiLDW4lq7E74HY/A/T9axOA73e7roCnxyDBT/Uj8HDQc5jlTw+ysDWPQL715WaEYTgBDspMgIQf5wFoOTsePxQUwaxjfCGZn44s71IWH94GEIRVC5DFBtQKBckiW0CthBUEMPa+NwhuJYsfAkKomoNRtRb9DBD0acCnDe12O34ISINft2unP4qdw5EOPVr9fl8OHOBT8bwLoc8tt21y74sUPyvgyLwEtvwdmwDFPxLwGv4VFlAy/tktmuFX+cu7dIs2pMvpJwLwtiJ+3HJ1l3oGLPAOJAl+1PoFcCVr09AjwFY/AwwGwBa9BTkhADEBHoyAdgDs9XuEnx6QqGdT/tg8z0DKl882GOgbEL4F9ifAkXkJbG6Bj0yAkzH8IwFtRrCiCV269SwXfOb0em95l27RhnQ5EYAJboIBWWwQ7lgp9KP0ezB3zwn3mwBCrwTV8RCwmTvgNj8DDP1rEYB0B7w769II2KUIvV6vp/qxfXoU9ax8Jiuf5gi86Ct/9hAoOJPJT98C6/cAnYD2W4DiX8YEeH0N/6548jOBPwp0lU3pE8zMWa7lj8PlXQYL0uVEet1UrHYAE+HHLfgtiHx5JVnyYiM30JUquJUseQT42kBAqtYAWsm2bQWwQ/4RgDz/CYDknwGQ0ntfDH+cYxDuWfZ4D8/JvvOhAmgI1MwF86eP/waD0d4zwL0BUPALBCTswJ+b/6pMgGHyr4U4bPrIn+FKlr3YW5AupwQAEoGALLJj/xNkmQ4/arH4rPetCcsHEGilDG4l62XTCH+vjdwCd0Baufb8a89DwCcF0CQAqoB6/8v0iXrCoJ41+IdUQCJQ7WPvREDdhj9OCcTbYMHPCEjcIQB4cAtM8CmAQeCPAldV8gQ0BsqV/0PGgnQ5pfDv5uP3CuUDuFwuAVeqFouvqb8ImPcOBGKlbf0IuJL1AKHq7fX1P49vbnJ3XXkBAAAAAElFTkSuQmCC" />
                                        </td>
                                    </tr>
    
                                    <tr>
                                        <td colspan="2" style="height: 24px;"></td>
                                    </tr>
                                    <tr>
                                        <td colspan="2">
                                            <table cellpadding="0" cellspacing="0" border="0" style="width: 100%;">
                                                <tr>
                                                    <td id="header-logo" valign="top" style="padding-left: 16px;">
                                                        <img height="32" width="143" style="height: 32px; width: 143px;" src="data:image/png;base64,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" />
                                                    </td>
                                                    <td id="header-text" style="text-align: right; padding-right: 16px; mso-line-height-rule: exactly;">
                                                        <p
                                                            style="margin: 6px 0px; padding: 0px; font-size: 20px; line-height: 20px; font-weight: bold;">
                                                            Customer Notification
                                                        </p>
                                                        <p style="margin: 2px 0px; padding: 0px; font-size: 14px; line-height: 14px;">
                                                            BD Global Operation Center
                                                        </p>
                                                    </td>
                                                </tr>
                                            </table>
                                        </td>
                                    </tr>
                                    
                                    <tr>
                                        <td colspan="2" style="padding: 54px 16px 0px;">
                                            <h1 style="margin: 0px; font-size: 32px; line-height: 32px; font-weight: bold; text-align: center;">
                                                Disk C Usage Reached 99%
                                            </h1>
                                        </td>
                                    </tr>
                                    
                                    <tr>
                                        <td colspan="2" style="padding: 32px 16px 0px;">
                                            Dear System Owner,<br><br>During the last four hours, we have monitored your server <b>{}</b> is having a disk performance issue. The disk C usage gradually increased and reached a critical value <strong style="color:red">99%</strong>.<br><br>
                                            Please make sure that there are no <b>application data</b> (including log files) is stored on Disk C. If this is the case, please move application data to other discs. <br>
                                            Please delete the data or move it to other drives in order not to jeopardize the stability of the operating system.<br>
                                            Disk C is reserved for the operating system to ensure the stability of server operation.<br>
                                            You should do this as soon as possible to carry out, as otherwise there is a risk that the server is not working correctly.<br><br>
                                            If you need an additional data disk or enlarge the existing data disc, you can order this by the following ITSP Order Form: <i><a href="https://rb-servicecatalog.apps.intranet.bosch.com/RequestCenter/website/Grunt/application/offer.html?id=4369">Server Hosting – Server Change Request (Physical and Virtual)<span style='font-style:normal'>.</span></a></i><br>
                                            Thanks for your understanding and CI-Server-Opeartion-Center will continuously monitor your server.<br><br><br>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td colspan="2" style="height: 32px;"></td>
                                    </tr>
                                    <tr>
                                        <td colspan="2" style="height: 1px; background-color: #E0E2E5;"></td>
                                    </tr>
                                    <tr>
                                        <td class="dyn-col" valign="top"
                                            style="width: 50%; padding: 16px; font-size: 12px; line-height: 18px;">
                                            <b>Name and address</b>
                                            <br>
                                            Robert Bosch GmbH
                                            <br>
                                            Robert-Bosch-Platz 1
                                            <br>
                                            70839 Gerlingen-Schillerh&ouml;he
                                            <br>
                                            <br>
                                            <b>Board of management</b>
                                            <br>Dr.&nbsp;Stefan&nbsp;Hartung, Dr.&nbsp;Christian&nbsp;Fischer, Filiz&nbsp;Albrecht, Dr.&nbsp;Markus&nbsp;Forschner, Dr.&nbsp;Markus&nbsp;Heyn, Rolf&nbsp;Najork                          
                                        </td>
                                        <td class="dyn-col" valign="top"
                                            style="width: 50%; padding: 16px; font-size: 12px; line-height: 18px;">
                                            <b>Registration court</b>
                                            <br>
                                            District court Stuttgart HRB 14000
                                            <br>
                                            <br>
                                            <b>VAT identification number</b>
                                            <br>
                                            DE811128135
                                            <br>
                                            <br>
                                            <b>Your contact at Bosch</b>
                                            <br>
                                            <a href="mailto:ITServiceDesk@bosch.com">
                                                ITServiceDesk@bosch.com
                                            </a>
                                            <br>
                                            +49 (711) 811-3311
                                            <br>
                                            <br>
                                            <a href="https://www.bosch.de/datenschutzhinweise/?prevent-auto-open-privacy-settings=1">
                                                Data privacy policy
                                            </a>
                                        </td>
                                    </tr>
    
                                    <tr>
                                        <td colspan="2"
                                            style="padding: 8px 16px 16px; background-color: #EFF1F2; font-size: 12px; font-style: italic; line-height: 18px;">
                                            This is an automatically generated email. You are receiving it as member of the server used by.
                                        </td>
                                    </tr>
                                </table>
                            </td>
                        </tr>
                    </table>
                </body>
            </html>
            '''.format(host_name, '99')

    # Server reboot: Windows uptime 80 days
    elif email_type == '2':
        if incident:
            email_msg['subject'] = '[' + str(incident) + '] Detect your server has unusual system uptime: 80 days / ' + host_name
        else:
            email_msg['subject'] = 'Detect your server has unusual system uptime: 80 days / ' + host_name
        email_msg['content'] = '''
            <!DOCTYPE html>
            <html lang="en">
                <head>
                    <title>Unusual System Uptime: 80 days</title>
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
                    <meta name="color-scheme" content="only">
                    <meta http-equiv="X-Render-Mode" content="html">
                    <style type="text/css">
                        body {{font-size: 16px; line-height: 24px; font-family: Bosch Office Sans, Arial, sans-serif;}}
    
                        a {{text-decoration: none; color: #007BC0;}}
    
                        @media screen and (max-width: 640px) {{
                            #innerTable {{width: 320px !important;}}
    
                            #header-logo {{
                                display: block !important;
                                float: left !important;
                                width: 100% !important;
                            }}
    
                            #header-text {{
                                display: block !important;
                                float: left !important;
                                width: 100% !important;
                                text-align: left !important;
                                padding: 0px 0px 0px 16px !important;
                            }}
    
                            .dyn-col {{
                                display: block !important;
                                float: left !important;
                                width: 100% !important;
                                box-sizing: border-box !important;
                            }}
                        }}
    
                        @supports (-webkit-touch-callout: none) {{
                            body {{
                                background-color: #EFF1F2;
                            }}
                        }}
                    </style>
                </head>
    
                <body style="margin: 0px;">
                    <table id="outerTable" cellpadding="0" cellspacing="0" border="0" style="width: 100%; background-color: #EFF1F2;">
                        <tr>
                            <td>
                                <span
                                    style="color: #EFF1F2; display: none; opacity: 0; overflow: hidden; mso-hide: all; visibility: hidden;">
                                    Customer Notification - System Uptime: 80 days<br>
                                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                                </span>
    
                                <table id="innerTable" cellpadding="0" cellspacing="0" border="0" align="center" style="width: 640px; background-color: #FFF; margin-bottom: 16px;">
                                    <tr>
                                        <td colspan="2" style="line-height: 0px;">
                                            <img width="640" height="6" style="height: 6px; width: 100%;" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAABQAAAAAMCAMAAAAKwOAZAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAADwUExURZUkMp8kNLEnOa8gJMEhKtQgJ54vZn42hW03jWo4jWg4jmU5jmM5jmE6jl86jlw7jlk7j1c8j1M8j1A9j00+kEo+kEk/kEc/kEY/kERAkEJAkD9BkTxBkTo8gDc8gDU8fzM8fy89fiw9fSk9fSU+gyY8gig7gCo4hiNAhiVdoSZeoi9+tTmUwDijyzmjyzqkywWmywWetgqdXAqdXQqcXkGoZIm8blOuamKxbTKNRrAkMbIpTiM+hBClygWlywablB6iYjmfWzB+th2lyXu5bDKWULAiKy6kxweac2+2a4o1fQWlyidOljGNRjB/tgAAAJPcmuEAAABQdFJOU/////////////////////////////////////////////////////////////////////////////////////////////////////////8AE3OmeQAAAAlwSFlzAAAOwwAADsMBx2+oZAAABWBJREFUaEPd221v2lYYxvEpoQ30DXkZpIBIkICmhRCUjIx02bRm0oqWfv+Ps/vhOk9gE/v42HX3Pwfbadq3P9226S8NtD3pbKM+286p7V2ben929oGSw0Hn2LKwM7twGwt7r0HQ5aVuNBrOxmP+6D5o6q/DZvPcNa2y3m52vPnHFH2q1qKxVjV0t26oh18T9/BtQ+vhtwaCUXW2PYlvC/5OTzuwpxWdkHNZBLJ5WfxlKMjg2Y0VbC9x72JEH1qhf5eD2dA0HgI9L0+/8fRqcqV74pp/mWSv+RdpGrcKMAjp8gJh1QJksX0HT/X3O9BK2R/wKbL7oq3/hFvJ2jxSm79hVK0BqVoDZjG1FMB36l3mBOj4c0uyBCp79iKDQM4zkPzDGDgjAEMCB06/HAGvXEyfbjRl5ua85hO68D+kGJ2nymAMhHw4xiCgywuEVeuvan0GT7V32yIAwVqJ1nArWS8M4OP/BsCn+BmwpQA+feieCX/mozF2IiAMtOOffPZi8HTbhW1OtkviT6Y/NlDs80bAsS/gQVPQJzF9ukzWNxuRyCryL2gI5J+w5JellzKYGaDL698bIFalT5AssooA3hZvsVo9J271D0Qr1L2uqNbfAFeyeATcgKh6g1G1to0G0PnXroeA+ggwMyUwWLydgcqeHtw1FvZ+gxEryA6qfnn+ZRgI+6QD/zIA1GgEVLz4yv6Av21wK7R00zqYBAFdTvMU/v04AOFa4b5CrZSBtiLdyyG29A8BGcBGHgG2/BlgSwHs7GT+0yGQM2c7/Kl8OvvZ6c9eUI4/NU9O5hLbphPgTMbA/QnQAGj1CwkMJ0Ci75qWJ6CSlhP7J1OgEigbCJZhMDi5IF1OSQbAqrfA0KxMAK1sy+QD4HPhdyCsHyiLDW4lq7E74HY/A/T9axOA73e7roCnxyDBT/Uj8HDQc5jlTw+ysDWPQL715WaEYTgBDspMgIQf5wFoOTsePxQUwaxjfCGZn44s71IWH94GEIRVC5DFBtQKBckiW0CthBUEMPa+NwhuJYsfAkKomoNRtRb9DBD0acCnDe12O34ISINft2unP4qdw5EOPVr9fl8OHOBT8bwLoc8tt21y74sUPyvgyLwEtvwdmwDFPxLwGv4VFlAy/tktmuFX+cu7dIs2pMvpJwLwtiJ+3HJ1l3oGLPAOJAl+1PoFcCVr09AjwFY/AwwGwBa9BTkhADEBHoyAdgDs9XuEnx6QqGdT/tg8z0DKl882GOgbEL4F9ifAkXkJbG6Bj0yAkzH8IwFtRrCiCV269SwXfOb0em95l27RhnQ5EYAJboIBWWwQ7lgp9KP0ezB3zwn3mwBCrwTV8RCwmTvgNj8DDP1rEYB0B7w769II2KUIvV6vp/qxfXoU9ax8Jiuf5gi86Ct/9hAoOJPJT98C6/cAnYD2W4DiX8YEeH0N/6548jOBPwp0lU3pE8zMWa7lj8PlXQYL0uVEet1UrHYAE+HHLfgtiHx5JVnyYiM30JUquJUseQT42kBAqtYAWsm2bQWwQ/4RgDz/CYDknwGQ0ntfDH+cYxDuWfZ4D8/JvvOhAmgI1MwF86eP/waD0d4zwL0BUPALBCTswJ+b/6pMgGHyr4U4bPrIn+FKlr3YW5AupwQAEoGALLJj/xNkmQ4/arH4rPetCcsHEGilDG4l62XTCH+vjdwCd0Baufb8a89DwCcF0CQAqoB6/8v0iXrCoJ41+IdUQCJQ7WPvREDdhj9OCcTbYMHPCEjcIQB4cAtM8CmAQeCPAldV8gQ0BsqV/0PGgnQ5pfDv5uP3CuUDuFwuAVeqFouvqb8ImPcOBGKlbf0IuJL1AKHq7fX1P49vbnJ3XXkBAAAAAElFTkSuQmCC" />
                                        </td>
                                    </tr>
    
                                    <tr>
                                        <td colspan="2" style="height: 24px;"></td>
                                    </tr>
                                    <tr>
                                        <td colspan="2">
                                            <table cellpadding="0" cellspacing="0" border="0" style="width: 100%;">
                                                <tr>
                                                    <td id="header-logo" valign="top" style="padding-left: 16px;">
                                                        <img height="32" width="143" style="height: 32px; width: 143px;" src="data:image/png;base64,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" />
                                                    </td>
                                                    <td id="header-text" style="text-align: right; padding-right: 16px; mso-line-height-rule: exactly;">
                                                        <p
                                                            style="margin: 6px 0px; padding: 0px; font-size: 20px; line-height: 20px; font-weight: bold;">
                                                            Customer Notification
                                                        </p>
                                                        <p style="margin: 2px 0px; padding: 0px; font-size: 14px; line-height: 14px;">
                                                            BD Global Operation Center
                                                        </p>
                                                    </td>
                                                </tr>
                                            </table>
                                        </td>
                                    </tr>
                                    
                                    <tr>
                                        <td colspan="2" style="padding: 54px 16px 0px;">
                                            <h1 style="margin: 0px; font-size: 32px; line-height: 32px; font-weight: bold; text-align: center;">
                                                Unusual System Uptime: 80 days
                                            </h1>
                                        </td>
                                    </tr>
                                    
                                    <tr>
                                        <td colspan="2" style="padding: 32px 16px 0px;">
                                            Dear System Owner,<br><br>The mentioned server system <b>{}</b> is being detected for unusual uptime of <b>80</b> days.<br><br>
                                            To facilitate the next server patching for your system, a reboot is necessary to ensure the existing patch is up-to-date.<br>
                                            Please schedule a <b>system reboot</b> for your system through the following ITSP Order Form: <i><a href="https://rb-servicecatalog.apps.intranet.bosch.com/RequestCenter/website/Grunt/application/offer.html?id=4602">Server Hosting – Server Reboot<span style='font-style:normal'>.</span></a></i><br><br>
                                            After raising the ITSP Order form, kindly feedback via this e-mail on the ITSP order number.<br>
                                            BD Global Operation Center will check for the Windows Server updates and inform you if required further action.<br><br><br>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td colspan="2" style="height: 32px;"></td>
                                    </tr>
                                    <tr>
                                        <td colspan="2" style="height: 1px; background-color: #E0E2E5;"></td>
                                    </tr>
                                    <tr>
                                        <td class="dyn-col" valign="top"
                                            style="width: 50%; padding: 16px; font-size: 12px; line-height: 18px;">
                                            <b>Name and address</b>
                                            <br>
                                            Robert Bosch GmbH
                                            <br>
                                            Robert-Bosch-Platz 1
                                            <br>
                                            70839 Gerlingen-Schillerh&ouml;he
                                            <br>
                                            <br>
                                            <b>Board of management</b>
                                            <br>Dr.&nbsp;Stefan&nbsp;Hartung, Dr.&nbsp;Christian&nbsp;Fischer, Filiz&nbsp;Albrecht, Dr.&nbsp;Markus&nbsp;Forschner, Dr.&nbsp;Markus&nbsp;Heyn, Rolf&nbsp;Najork                          
                                        </td>
                                        <td class="dyn-col" valign="top"
                                            style="width: 50%; padding: 16px; font-size: 12px; line-height: 18px;">
                                            <b>Registration court</b>
                                            <br>
                                            District court Stuttgart HRB 14000
                                            <br>
                                            <br>
                                            <b>VAT identification number</b>
                                            <br>
                                            DE811128135
                                            <br>
                                            <br>
                                            <b>Your contact at Bosch</b>
                                            <br>
                                            <a href="mailto:ITServiceDesk@bosch.com">
                                                ITServiceDesk@bosch.com
                                            </a>
                                            <br>
                                            +49 (711) 811-3311
                                            <br>
                                            <br>
                                            <a href="https://www.bosch.de/datenschutzhinweise/?prevent-auto-open-privacy-settings=1">
                                                Data privacy policy
                                            </a>
                                        </td>
                                    </tr>
    
                                    <tr>
                                        <td colspan="2"
                                            style="padding: 8px 16px 16px; background-color: #EFF1F2; font-size: 12px; font-style: italic; line-height: 18px;">
                                            This is an automatically generated email. You are receiving it as member of the server used by.
                                        </td>
                                    </tr>
                                </table>
                            </td>
                        </tr>
                    </table>
                </body>
            </html>
            '''.format(host_name)

    # Server reboot: Windows update
    elif email_type == '3':
        if incident:
            email_msg['subject'] = '[' + str(incident) + '] Server needs a reboot to apply the latest Windows Update / ' + host_name
        else:
            email_msg['subject'] = 'Server needs a reboot to apply the latest Windows Update / ' + host_name
        email_msg['content'] = '''
            <!DOCTYPE html>
            <html lang="en">
                <head>
                    <title>Windows Update Failed</title>
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
                    <meta name="color-scheme" content="only">
                    <meta http-equiv="X-Render-Mode" content="html">
                    <style type="text/css">
                        body {{font-size: 16px; line-height: 24px; font-family: Bosch Office Sans, Arial, sans-serif;}}
    
                        a {{text-decoration: none; color: #007BC0;}}
    
                        @media screen and (max-width: 640px) {{
                            #innerTable {{width: 320px !important;}}
    
                            #header-logo {{
                                display: block !important;
                                float: left !important;
                                width: 100% !important;
                            }}
    
                            #header-text {{
                                display: block !important;
                                float: left !important;
                                width: 100% !important;
                                text-align: left !important;
                                padding: 0px 0px 0px 16px !important;
                            }}
    
                            .dyn-col {{
                                display: block !important;
                                float: left !important;
                                width: 100% !important;
                                box-sizing: border-box !important;
                            }}
                        }}
    
                        @supports (-webkit-touch-callout: none) {{
                            body {{
                                background-color: #EFF1F2;
                            }}
                        }}
                    </style>
                </head>
    
                <body style="margin: 0px;">
                    <table id="outerTable" cellpadding="0" cellspacing="0" border="0" style="width: 100%; background-color: #EFF1F2;">
                        <tr>
                            <td>
                                <span
                                    style="color: #EFF1F2; display: none; opacity: 0; overflow: hidden; mso-hide: all; visibility: hidden;">
                                    Customer Notification - Windows Update Failed<br>
                                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                                </span>
    
                                <table id="innerTable" cellpadding="0" cellspacing="0" border="0" align="center" style="width: 640px; background-color: #FFF; margin-bottom: 16px;">
                                    <tr>
                                        <td colspan="2" style="line-height: 0px;">
                                            <img width="640" height="6" style="height: 6px; width: 100%;" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAABQAAAAAMCAMAAAAKwOAZAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAADwUExURZUkMp8kNLEnOa8gJMEhKtQgJ54vZn42hW03jWo4jWg4jmU5jmM5jmE6jl86jlw7jlk7j1c8j1M8j1A9j00+kEo+kEk/kEc/kEY/kERAkEJAkD9BkTxBkTo8gDc8gDU8fzM8fy89fiw9fSk9fSU+gyY8gig7gCo4hiNAhiVdoSZeoi9+tTmUwDijyzmjyzqkywWmywWetgqdXAqdXQqcXkGoZIm8blOuamKxbTKNRrAkMbIpTiM+hBClygWlywablB6iYjmfWzB+th2lyXu5bDKWULAiKy6kxweac2+2a4o1fQWlyidOljGNRjB/tgAAAJPcmuEAAABQdFJOU/////////////////////////////////////////////////////////////////////////////////////////////////////////8AE3OmeQAAAAlwSFlzAAAOwwAADsMBx2+oZAAABWBJREFUaEPd221v2lYYxvEpoQ30DXkZpIBIkICmhRCUjIx02bRm0oqWfv+Ps/vhOk9gE/v42HX3Pwfbadq3P9226S8NtD3pbKM+286p7V2ben929oGSw0Hn2LKwM7twGwt7r0HQ5aVuNBrOxmP+6D5o6q/DZvPcNa2y3m52vPnHFH2q1qKxVjV0t26oh18T9/BtQ+vhtwaCUXW2PYlvC/5OTzuwpxWdkHNZBLJ5WfxlKMjg2Y0VbC9x72JEH1qhf5eD2dA0HgI9L0+/8fRqcqV74pp/mWSv+RdpGrcKMAjp8gJh1QJksX0HT/X3O9BK2R/wKbL7oq3/hFvJ2jxSm79hVK0BqVoDZjG1FMB36l3mBOj4c0uyBCp79iKDQM4zkPzDGDgjAEMCB06/HAGvXEyfbjRl5ua85hO68D+kGJ2nymAMhHw4xiCgywuEVeuvan0GT7V32yIAwVqJ1nArWS8M4OP/BsCn+BmwpQA+feieCX/mozF2IiAMtOOffPZi8HTbhW1OtkviT6Y/NlDs80bAsS/gQVPQJzF9ukzWNxuRyCryL2gI5J+w5JellzKYGaDL698bIFalT5AssooA3hZvsVo9J271D0Qr1L2uqNbfAFeyeATcgKh6g1G1to0G0PnXroeA+ggwMyUwWLydgcqeHtw1FvZ+gxEryA6qfnn+ZRgI+6QD/zIA1GgEVLz4yv6Av21wK7R00zqYBAFdTvMU/v04AOFa4b5CrZSBtiLdyyG29A8BGcBGHgG2/BlgSwHs7GT+0yGQM2c7/Kl8OvvZ6c9eUI4/NU9O5hLbphPgTMbA/QnQAGj1CwkMJ0Ci75qWJ6CSlhP7J1OgEigbCJZhMDi5IF1OSQbAqrfA0KxMAK1sy+QD4HPhdyCsHyiLDW4lq7E74HY/A/T9axOA73e7roCnxyDBT/Uj8HDQc5jlTw+ysDWPQL715WaEYTgBDspMgIQf5wFoOTsePxQUwaxjfCGZn44s71IWH94GEIRVC5DFBtQKBckiW0CthBUEMPa+NwhuJYsfAkKomoNRtRb9DBD0acCnDe12O34ISINft2unP4qdw5EOPVr9fl8OHOBT8bwLoc8tt21y74sUPyvgyLwEtvwdmwDFPxLwGv4VFlAy/tktmuFX+cu7dIs2pMvpJwLwtiJ+3HJ1l3oGLPAOJAl+1PoFcCVr09AjwFY/AwwGwBa9BTkhADEBHoyAdgDs9XuEnx6QqGdT/tg8z0DKl882GOgbEL4F9ifAkXkJbG6Bj0yAkzH8IwFtRrCiCV269SwXfOb0em95l27RhnQ5EYAJboIBWWwQ7lgp9KP0ezB3zwn3mwBCrwTV8RCwmTvgNj8DDP1rEYB0B7w769II2KUIvV6vp/qxfXoU9ax8Jiuf5gi86Ct/9hAoOJPJT98C6/cAnYD2W4DiX8YEeH0N/6548jOBPwp0lU3pE8zMWa7lj8PlXQYL0uVEet1UrHYAE+HHLfgtiHx5JVnyYiM30JUquJUseQT42kBAqtYAWsm2bQWwQ/4RgDz/CYDknwGQ0ntfDH+cYxDuWfZ4D8/JvvOhAmgI1MwF86eP/waD0d4zwL0BUPALBCTswJ+b/6pMgGHyr4U4bPrIn+FKlr3YW5AupwQAEoGALLJj/xNkmQ4/arH4rPetCcsHEGilDG4l62XTCH+vjdwCd0Baufb8a89DwCcF0CQAqoB6/8v0iXrCoJ41+IdUQCJQ7WPvREDdhj9OCcTbYMHPCEjcIQB4cAtM8CmAQeCPAldV8gQ0BsqV/0PGgnQ5pfDv5uP3CuUDuFwuAVeqFouvqb8ImPcOBGKlbf0IuJL1AKHq7fX1P49vbnJ3XXkBAAAAAElFTkSuQmCC" />
                                        </td>
                                    </tr>
    
                                    <tr>
                                        <td colspan="2" style="height: 24px;"></td>
                                    </tr>
                                    <tr>
                                        <td colspan="2">
                                            <table cellpadding="0" cellspacing="0" border="0" style="width: 100%;">
                                                <tr>
                                                    <td id="header-logo" valign="top" style="padding-left: 16px;">
                                                        <img height="32" width="143" style="height: 32px; width: 143px;" src="data:image/png;base64,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" />
                                                    </td>
                                                    <td id="header-text" style="text-align: right; padding-right: 16px; mso-line-height-rule: exactly;">
                                                        <p
                                                            style="margin: 6px 0px; padding: 0px; font-size: 20px; line-height: 20px; font-weight: bold;">
                                                            Customer Notification
                                                        </p>
                                                        <p style="margin: 2px 0px; padding: 0px; font-size: 14px; line-height: 14px;">
                                                            BD Global Operation Center
                                                        </p>
                                                    </td>
                                                </tr>
                                            </table>
                                        </td>
                                    </tr>
                                    
                                    <tr>
                                        <td colspan="2" style="padding: 54px 16px 0px;">
                                            <h1 style="margin: 0px; font-size: 32px; line-height: 32px; font-weight: bold; text-align: center;">
                                                Windows Update Failed
                                            </h1>
                                        </td>
                                    </tr>
                                    
                                    <tr>
                                        <td colspan="2" style="padding: 32px 16px 0px;">
                                            Dear System Owner,<br><br>The mentioned server system <b>{}</b> was failed to install Windows update at last time, and we have applied them manually.<br><br>
                                            To facilitate the next server patching for your system, a reboot is necessary to ensure the existing patch is up-to-date.<br>
                                            Please schedule a <b>system reboot</b> for your system through the following ITSP Order Form: <i><a href="https://rb-servicecatalog.apps.intranet.bosch.com/RequestCenter/website/Grunt/application/offer.html?id=4602">Server Hosting – Server Reboot<span style='font-style:normal'>.</span></a></i><br><br>
                                            After raising the ITSP Order form, kindly feedback via this e-mail on the ITSP order number.<br>
                                            BD Global Operation Center will check for the Windows Server updates and inform you if required further action.<br><br><br>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td colspan="2" style="height: 32px;"></td>
                                    </tr>
                                    <tr>
                                        <td colspan="2" style="height: 1px; background-color: #E0E2E5;"></td>
                                    </tr>
                                    <tr>
                                        <td class="dyn-col" valign="top"
                                            style="width: 50%; padding: 16px; font-size: 12px; line-height: 18px;">
                                            <b>Name and address</b>
                                            <br>
                                            Robert Bosch GmbH
                                            <br>
                                            Robert-Bosch-Platz 1
                                            <br>
                                            70839 Gerlingen-Schillerh&ouml;he
                                            <br>
                                            <br>
                                            <b>Board of management</b>
                                            <br>Dr.&nbsp;Stefan&nbsp;Hartung, Dr.&nbsp;Christian&nbsp;Fischer, Filiz&nbsp;Albrecht, Dr.&nbsp;Markus&nbsp;Forschner, Dr.&nbsp;Markus&nbsp;Heyn, Rolf&nbsp;Najork                          
                                        </td>
                                        <td class="dyn-col" valign="top"
                                            style="width: 50%; padding: 16px; font-size: 12px; line-height: 18px;">
                                            <b>Registration court</b>
                                            <br>
                                            District court Stuttgart HRB 14000
                                            <br>
                                            <br>
                                            <b>VAT identification number</b>
                                            <br>
                                            DE811128135
                                            <br>
                                            <br>
                                            <b>Your contact at Bosch</b>
                                            <br>
                                            <a href="mailto:ITServiceDesk@bosch.com">
                                                ITServiceDesk@bosch.com
                                            </a>
                                            <br>
                                            +49 (711) 811-3311
                                            <br>
                                            <br>
                                            <a href="https://www.bosch.de/datenschutzhinweise/?prevent-auto-open-privacy-settings=1">
                                                Data privacy policy
                                            </a>
                                        </td>
                                    </tr>
    
                                    <tr>
                                        <td colspan="2"
                                            style="padding: 8px 16px 16px; background-color: #EFF1F2; font-size: 12px; font-style: italic; line-height: 18px;">
                                            This is an automatically generated email. You are receiving it as member of the server used by.
                                        </td>
                                    </tr>
                                </table>
                            </td>
                        </tr>
                    </table>
                </body>
            </html>
            '''.format(host_name)

    # Server reboot: System hung
    elif email_type == '4':
        if incident:
            email_msg['subject'] = '[' + str(
                incident) + '] Server down alert received for ' + host_name
        else:
            email_msg['subject'] = 'Server down alert received for ' + host_name
        email_msg['content'] = '''
                <!DOCTYPE html>
                <html lang="en">
                    <head>
                        <title>Server down alert</title>
                        <meta name="viewport" content="width=device-width, initial-scale=1.0">
                        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
                        <meta name="color-scheme" content="only">
                        <meta http-equiv="X-Render-Mode" content="html">
                        <style type="text/css">
                            body {{font-size: 16px; line-height: 24px; font-family: Bosch Office Sans, Arial, sans-serif;}}

                            a {{text-decoration: none; color: #007BC0;}}

                            @media screen and (max-width: 640px) {{
                                #innerTable {{width: 320px !important;}}

                                #header-logo {{
                                    display: block !important;
                                    float: left !important;
                                    width: 100% !important;
                                }}

                                #header-text {{
                                    display: block !important;
                                    float: left !important;
                                    width: 100% !important;
                                    text-align: left !important;
                                    padding: 0px 0px 0px 16px !important;
                                }}

                                .dyn-col {{
                                    display: block !important;
                                    float: left !important;
                                    width: 100% !important;
                                    box-sizing: border-box !important;
                                }}
                            }}

                            @supports (-webkit-touch-callout: none) {{
                                body {{
                                    background-color: #EFF1F2;
                                }}
                            }}
                        </style>
                    </head>

                    <body style="margin: 0px;">
                        <table id="outerTable" cellpadding="0" cellspacing="0" border="0" style="width: 100%; background-color: #EFF1F2;">
                            <tr>
                                <td>
                                    <span
                                        style="color: #EFF1F2; display: none; opacity: 0; overflow: hidden; mso-hide: all; visibility: hidden;">
                                        Customer Notification - Server Down<br>
                                        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                                    </span>

                                    <table id="innerTable" cellpadding="0" cellspacing="0" border="0" align="center" style="width: 640px; background-color: #FFF; margin-bottom: 16px;">
                                        <tr>
                                            <td colspan="2" style="line-height: 0px;">
                                                <img width="640" height="6" style="height: 6px; width: 100%;" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAABQAAAAAMCAMAAAAKwOAZAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAADwUExURZUkMp8kNLEnOa8gJMEhKtQgJ54vZn42hW03jWo4jWg4jmU5jmM5jmE6jl86jlw7jlk7j1c8j1M8j1A9j00+kEo+kEk/kEc/kEY/kERAkEJAkD9BkTxBkTo8gDc8gDU8fzM8fy89fiw9fSk9fSU+gyY8gig7gCo4hiNAhiVdoSZeoi9+tTmUwDijyzmjyzqkywWmywWetgqdXAqdXQqcXkGoZIm8blOuamKxbTKNRrAkMbIpTiM+hBClygWlywablB6iYjmfWzB+th2lyXu5bDKWULAiKy6kxweac2+2a4o1fQWlyidOljGNRjB/tgAAAJPcmuEAAABQdFJOU/////////////////////////////////////////////////////////////////////////////////////////////////////////8AE3OmeQAAAAlwSFlzAAAOwwAADsMBx2+oZAAABWBJREFUaEPd221v2lYYxvEpoQ30DXkZpIBIkICmhRCUjIx02bRm0oqWfv+Ps/vhOk9gE/v42HX3Pwfbadq3P9226S8NtD3pbKM+286p7V2ben929oGSw0Hn2LKwM7twGwt7r0HQ5aVuNBrOxmP+6D5o6q/DZvPcNa2y3m52vPnHFH2q1qKxVjV0t26oh18T9/BtQ+vhtwaCUXW2PYlvC/5OTzuwpxWdkHNZBLJ5WfxlKMjg2Y0VbC9x72JEH1qhf5eD2dA0HgI9L0+/8fRqcqV74pp/mWSv+RdpGrcKMAjp8gJh1QJksX0HT/X3O9BK2R/wKbL7oq3/hFvJ2jxSm79hVK0BqVoDZjG1FMB36l3mBOj4c0uyBCp79iKDQM4zkPzDGDgjAEMCB06/HAGvXEyfbjRl5ua85hO68D+kGJ2nymAMhHw4xiCgywuEVeuvan0GT7V32yIAwVqJ1nArWS8M4OP/BsCn+BmwpQA+feieCX/mozF2IiAMtOOffPZi8HTbhW1OtkviT6Y/NlDs80bAsS/gQVPQJzF9ukzWNxuRyCryL2gI5J+w5JellzKYGaDL698bIFalT5AssooA3hZvsVo9J271D0Qr1L2uqNbfAFeyeATcgKh6g1G1to0G0PnXroeA+ggwMyUwWLydgcqeHtw1FvZ+gxEryA6qfnn+ZRgI+6QD/zIA1GgEVLz4yv6Av21wK7R00zqYBAFdTvMU/v04AOFa4b5CrZSBtiLdyyG29A8BGcBGHgG2/BlgSwHs7GT+0yGQM2c7/Kl8OvvZ6c9eUI4/NU9O5hLbphPgTMbA/QnQAGj1CwkMJ0Ci75qWJ6CSlhP7J1OgEigbCJZhMDi5IF1OSQbAqrfA0KxMAK1sy+QD4HPhdyCsHyiLDW4lq7E74HY/A/T9axOA73e7roCnxyDBT/Uj8HDQc5jlTw+ysDWPQL715WaEYTgBDspMgIQf5wFoOTsePxQUwaxjfCGZn44s71IWH94GEIRVC5DFBtQKBckiW0CthBUEMPa+NwhuJYsfAkKomoNRtRb9DBD0acCnDe12O34ISINft2unP4qdw5EOPVr9fl8OHOBT8bwLoc8tt21y74sUPyvgyLwEtvwdmwDFPxLwGv4VFlAy/tktmuFX+cu7dIs2pMvpJwLwtiJ+3HJ1l3oGLPAOJAl+1PoFcCVr09AjwFY/AwwGwBa9BTkhADEBHoyAdgDs9XuEnx6QqGdT/tg8z0DKl882GOgbEL4F9ifAkXkJbG6Bj0yAkzH8IwFtRrCiCV269SwXfOb0em95l27RhnQ5EYAJboIBWWwQ7lgp9KP0ezB3zwn3mwBCrwTV8RCwmTvgNj8DDP1rEYB0B7w769II2KUIvV6vp/qxfXoU9ax8Jiuf5gi86Ct/9hAoOJPJT98C6/cAnYD2W4DiX8YEeH0N/6548jOBPwp0lU3pE8zMWa7lj8PlXQYL0uVEet1UrHYAE+HHLfgtiHx5JVnyYiM30JUquJUseQT42kBAqtYAWsm2bQWwQ/4RgDz/CYDknwGQ0ntfDH+cYxDuWfZ4D8/JvvOhAmgI1MwF86eP/waD0d4zwL0BUPALBCTswJ+b/6pMgGHyr4U4bPrIn+FKlr3YW5AupwQAEoGALLJj/xNkmQ4/arH4rPetCcsHEGilDG4l62XTCH+vjdwCd0Baufb8a89DwCcF0CQAqoB6/8v0iXrCoJ41+IdUQCJQ7WPvREDdhj9OCcTbYMHPCEjcIQB4cAtM8CmAQeCPAldV8gQ0BsqV/0PGgnQ5pfDv5uP3CuUDuFwuAVeqFouvqb8ImPcOBGKlbf0IuJL1AKHq7fX1P49vbnJ3XXkBAAAAAElFTkSuQmCC" />
                                            </td>
                                        </tr>

                                        <tr>
                                            <td colspan="2" style="height: 24px;"></td>
                                        </tr>
                                        <tr>
                                            <td colspan="2">
                                                <table cellpadding="0" cellspacing="0" border="0" style="width: 100%;">
                                                    <tr>
                                                        <td id="header-logo" valign="top" style="padding-left: 16px;">
                                                            <img height="32" width="143" style="height: 32px; width: 143px;" src="data:image/png;base64,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" />
                                                        </td>
                                                        <td id="header-text" style="text-align: right; padding-right: 16px; mso-line-height-rule: exactly;">
                                                            <p
                                                                style="margin: 6px 0px; padding: 0px; font-size: 20px; line-height: 20px; font-weight: bold;">
                                                                Customer Notification
                                                            </p>
                                                            <p style="margin: 2px 0px; padding: 0px; font-size: 14px; line-height: 14px;">
                                                                BD Global Operation Center
                                                            </p>
                                                        </td>
                                                    </tr>
                                                </table>
                                            </td>
                                        </tr>

                                        <tr>
                                            <td colspan="2" style="padding: 54px 16px 0px;">
                                                <h1 style="margin: 0px; font-size: 32px; line-height: 32px; font-weight: bold; text-align: center;">
                                                    Server Down
                                                </h1>
                                            </td>
                                        </tr>

                                        <tr>
                                            <td colspan="2" style="padding: 32px 16px 0px;">
                                                Dear System Owner,<br><br>Please be informed that we received server down alert for the mentioned server system <b>{}</b>.<br>
                                                To resolve the issue we have to reboot above mentioned server.<br><br>
                                                Please kindly provide a time frame when we might perform a reboot for the above-mentioned server.<br>
                                                Also please take into consideration that server will be restarted if we do not receive any answer during the next hour.<br><br>
                                                BD Global Operation Center will check for the system and inform you if required further action.<br><br><br>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td colspan="2" style="height: 32px;"></td>
                                        </tr>
                                        <tr>
                                            <td colspan="2" style="height: 1px; background-color: #E0E2E5;"></td>
                                        </tr>
                                        <tr>
                                            <td class="dyn-col" valign="top"
                                                style="width: 50%; padding: 16px; font-size: 12px; line-height: 18px;">
                                                <b>Name and address</b>
                                                <br>
                                                Robert Bosch GmbH
                                                <br>
                                                Robert-Bosch-Platz 1
                                                <br>
                                                70839 Gerlingen-Schillerh&ouml;he
                                                <br>
                                                <br>
                                                <b>Board of management</b>
                                                <br>Dr.&nbsp;Stefan&nbsp;Hartung, Dr.&nbsp;Christian&nbsp;Fischer, Filiz&nbsp;Albrecht, Dr.&nbsp;Markus&nbsp;Forschner, Dr.&nbsp;Markus&nbsp;Heyn, Rolf&nbsp;Najork                          
                                            </td>
                                            <td class="dyn-col" valign="top"
                                                style="width: 50%; padding: 16px; font-size: 12px; line-height: 18px;">
                                                <b>Registration court</b>
                                                <br>
                                                District court Stuttgart HRB 14000
                                                <br>
                                                <br>
                                                <b>VAT identification number</b>
                                                <br>
                                                DE811128135
                                                <br>
                                                <br>
                                                <b>Your contact at Bosch</b>
                                                <br>
                                                <a href="mailto:ITServiceDesk@bosch.com">
                                                    ITServiceDesk@bosch.com
                                                </a>
                                                <br>
                                                +49 (711) 811-3311
                                                <br>
                                                <br>
                                                <a href="https://www.bosch.de/datenschutzhinweise/?prevent-auto-open-privacy-settings=1">
                                                    Data privacy policy
                                                </a>
                                            </td>
                                        </tr>

                                        <tr>
                                            <td colspan="2"
                                                style="padding: 8px 16px 16px; background-color: #EFF1F2; font-size: 12px; font-style: italic; line-height: 18px;">
                                                This is an automatically generated email. You are receiving it as member of the server used by.
                                            </td>
                                        </tr>
                                    </table>
                                </td>
                            </tr>
                        </table>
                    </body>
                </html>
                '''.format(host_name)

    # Windows Additional Software installation
    elif email_type == '5':
        if incident:
            email_msg['subject'] = '[' + str(
                incident) + '] Windows Additional Software installation for ' + host_name
        else:
            email_msg['subject'] = 'Windows Additional Software installation for ' + host_name
        email_msg['content'] = '''
                    <!DOCTYPE html>
                    <html lang="en">
                        <head>
                            <title>Additional Software Installation</title>
                            <meta name="viewport" content="width=device-width, initial-scale=1.0">
                            <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
                            <meta name="color-scheme" content="only">
                            <meta http-equiv="X-Render-Mode" content="html">
                            <style type="text/css">
                                body {{font-size: 16px; line-height: 24px; font-family: Bosch Office Sans, Arial, sans-serif;}}
    
                                a {{text-decoration: none; color: #007BC0;}}
    
                                @media screen and (max-width: 640px) {{
                                    #innerTable {{width: 320px !important;}}
    
                                    #header-logo {{
                                        display: block !important;
                                        float: left !important;
                                        width: 100% !important;
                                    }}
    
                                    #header-text {{
                                        display: block !important;
                                        float: left !important;
                                        width: 100% !important;
                                        text-align: left !important;
                                        padding: 0px 0px 0px 16px !important;
                                    }}
    
                                    .dyn-col {{
                                        display: block !important;
                                        float: left !important;
                                        width: 100% !important;
                                        box-sizing: border-box !important;
                                    }}
                                }}
    
                                @supports (-webkit-touch-callout: none) {{
                                    body {{
                                        background-color: #EFF1F2;
                                    }}
                                }}
                            </style>
                        </head>
    
                        <body style="margin: 0px;">
                            <table id="outerTable" cellpadding="0" cellspacing="0" border="0" style="width: 100%; background-color: #EFF1F2;">
                                <tr>
                                    <td>
                                        <span
                                            style="color: #EFF1F2; display: none; opacity: 0; overflow: hidden; mso-hide: all; visibility: hidden;">
                                            Customer Notification - Additional Software Installation<br>
                                            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                                        </span>
    
                                        <table id="innerTable" cellpadding="0" cellspacing="0" border="0" align="center" style="width: 640px; background-color: #FFF; margin-bottom: 16px;">
                                            <tr>
                                                <td colspan="2" style="line-height: 0px;">
                                                    <img width="640" height="6" style="height: 6px; width: 100%;" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAABQAAAAAMCAMAAAAKwOAZAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAADwUExURZUkMp8kNLEnOa8gJMEhKtQgJ54vZn42hW03jWo4jWg4jmU5jmM5jmE6jl86jlw7jlk7j1c8j1M8j1A9j00+kEo+kEk/kEc/kEY/kERAkEJAkD9BkTxBkTo8gDc8gDU8fzM8fy89fiw9fSk9fSU+gyY8gig7gCo4hiNAhiVdoSZeoi9+tTmUwDijyzmjyzqkywWmywWetgqdXAqdXQqcXkGoZIm8blOuamKxbTKNRrAkMbIpTiM+hBClygWlywablB6iYjmfWzB+th2lyXu5bDKWULAiKy6kxweac2+2a4o1fQWlyidOljGNRjB/tgAAAJPcmuEAAABQdFJOU/////////////////////////////////////////////////////////////////////////////////////////////////////////8AE3OmeQAAAAlwSFlzAAAOwwAADsMBx2+oZAAABWBJREFUaEPd221v2lYYxvEpoQ30DXkZpIBIkICmhRCUjIx02bRm0oqWfv+Ps/vhOk9gE/v42HX3Pwfbadq3P9226S8NtD3pbKM+286p7V2ben929oGSw0Hn2LKwM7twGwt7r0HQ5aVuNBrOxmP+6D5o6q/DZvPcNa2y3m52vPnHFH2q1qKxVjV0t26oh18T9/BtQ+vhtwaCUXW2PYlvC/5OTzuwpxWdkHNZBLJ5WfxlKMjg2Y0VbC9x72JEH1qhf5eD2dA0HgI9L0+/8fRqcqV74pp/mWSv+RdpGrcKMAjp8gJh1QJksX0HT/X3O9BK2R/wKbL7oq3/hFvJ2jxSm79hVK0BqVoDZjG1FMB36l3mBOj4c0uyBCp79iKDQM4zkPzDGDgjAEMCB06/HAGvXEyfbjRl5ua85hO68D+kGJ2nymAMhHw4xiCgywuEVeuvan0GT7V32yIAwVqJ1nArWS8M4OP/BsCn+BmwpQA+feieCX/mozF2IiAMtOOffPZi8HTbhW1OtkviT6Y/NlDs80bAsS/gQVPQJzF9ukzWNxuRyCryL2gI5J+w5JellzKYGaDL698bIFalT5AssooA3hZvsVo9J271D0Qr1L2uqNbfAFeyeATcgKh6g1G1to0G0PnXroeA+ggwMyUwWLydgcqeHtw1FvZ+gxEryA6qfnn+ZRgI+6QD/zIA1GgEVLz4yv6Av21wK7R00zqYBAFdTvMU/v04AOFa4b5CrZSBtiLdyyG29A8BGcBGHgG2/BlgSwHs7GT+0yGQM2c7/Kl8OvvZ6c9eUI4/NU9O5hLbphPgTMbA/QnQAGj1CwkMJ0Ci75qWJ6CSlhP7J1OgEigbCJZhMDi5IF1OSQbAqrfA0KxMAK1sy+QD4HPhdyCsHyiLDW4lq7E74HY/A/T9axOA73e7roCnxyDBT/Uj8HDQc5jlTw+ysDWPQL715WaEYTgBDspMgIQf5wFoOTsePxQUwaxjfCGZn44s71IWH94GEIRVC5DFBtQKBckiW0CthBUEMPa+NwhuJYsfAkKomoNRtRb9DBD0acCnDe12O34ISINft2unP4qdw5EOPVr9fl8OHOBT8bwLoc8tt21y74sUPyvgyLwEtvwdmwDFPxLwGv4VFlAy/tktmuFX+cu7dIs2pMvpJwLwtiJ+3HJ1l3oGLPAOJAl+1PoFcCVr09AjwFY/AwwGwBa9BTkhADEBHoyAdgDs9XuEnx6QqGdT/tg8z0DKl882GOgbEL4F9ifAkXkJbG6Bj0yAkzH8IwFtRrCiCV269SwXfOb0em95l27RhnQ5EYAJboIBWWwQ7lgp9KP0ezB3zwn3mwBCrwTV8RCwmTvgNj8DDP1rEYB0B7w769II2KUIvV6vp/qxfXoU9ax8Jiuf5gi86Ct/9hAoOJPJT98C6/cAnYD2W4DiX8YEeH0N/6548jOBPwp0lU3pE8zMWa7lj8PlXQYL0uVEet1UrHYAE+HHLfgtiHx5JVnyYiM30JUquJUseQT42kBAqtYAWsm2bQWwQ/4RgDz/CYDknwGQ0ntfDH+cYxDuWfZ4D8/JvvOhAmgI1MwF86eP/waD0d4zwL0BUPALBCTswJ+b/6pMgGHyr4U4bPrIn+FKlr3YW5AupwQAEoGALLJj/xNkmQ4/arH4rPetCcsHEGilDG4l62XTCH+vjdwCd0Baufb8a89DwCcF0CQAqoB6/8v0iXrCoJ41+IdUQCJQ7WPvREDdhj9OCcTbYMHPCEjcIQB4cAtM8CmAQeCPAldV8gQ0BsqV/0PGgnQ5pfDv5uP3CuUDuFwuAVeqFouvqb8ImPcOBGKlbf0IuJL1AKHq7fX1P49vbnJ3XXkBAAAAAElFTkSuQmCC" />
                                                </td>
                                            </tr>
    
                                            <tr>
                                                <td colspan="2" style="height: 24px;"></td>
                                            </tr>
                                            <tr>
                                                <td colspan="2">
                                                    <table cellpadding="0" cellspacing="0" border="0" style="width: 100%;">
                                                        <tr>
                                                            <td id="header-logo" valign="top" style="padding-left: 16px;">
                                                                <img height="32" width="143" style="height: 32px; width: 143px;" src="data:image/png;base64,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" />
                                                            </td>
                                                            <td id="header-text" style="text-align: right; padding-right: 16px; mso-line-height-rule: exactly;">
                                                                <p
                                                                    style="margin: 6px 0px; padding: 0px; font-size: 20px; line-height: 20px; font-weight: bold;">
                                                                    Customer Notification
                                                                </p>
                                                                <p style="margin: 2px 0px; padding: 0px; font-size: 14px; line-height: 14px;">
                                                                    BD Global Operation Center
                                                                </p>
                                                            </td>
                                                        </tr>
                                                    </table>
                                                </td>
                                            </tr>
    
                                            <tr>
                                                <td colspan="2" style="padding: 54px 16px 0px;">
                                                    <h1 style="margin: 0px; font-size: 32px; line-height: 32px; font-weight: bold; text-align: center;">
                                                        Additional Software Installation
                                                    </h1>
                                                </td>
                                            </tr>
    
                                            <tr>
                                                <td colspan="2" style="padding: 32px 16px 0px;">
                                                    Dear Customer,<br><br>The server data (including additional software installation) is managed by the server owners/users. 
                                                    BD/PI department is only responsible for the maintenance of server OS (operation system) & HW (hardware).<br>
                                                    Please contact server owner to install:<br>
                                                    {}<br><br>
                                                    Some necessary resources can be found in the following share:<br>
                                                    \\\\rb-winsystech.bosch.com\\download$\\<br>
                                                    \\\\sgpkms01.apac.bosch.com\\download$\\<br><br>
                                                    Any additional license should be purchased by server user self. More information please refer:<br>
                                                    <i><a href="https://inside-docupedia.bosch.com/confluence/display/CSO/Installation+and+Support+of+Additional+Windows+Components">Installation and Support of Additional Windows Components<span style='font-style:normal'>.</span></a></i>
                                                    <br><br>
                                                    Thanks for your understanding and cooperation.<br>
                                                </td>
                                            </tr>
                                            <tr>
                                                <td colspan="2" style="height: 32px;"></td>
                                            </tr>
                                            <tr>
                                                <td colspan="2" style="height: 1px; background-color: #E0E2E5;"></td>
                                            </tr>
                                            <tr>
                                                <td class="dyn-col" valign="top"
                                                    style="width: 50%; padding: 16px; font-size: 12px; line-height: 18px;">
                                                    <b>Name and address</b>
                                                    <br>
                                                    Robert Bosch GmbH
                                                    <br>
                                                    Robert-Bosch-Platz 1
                                                    <br>
                                                    70839 Gerlingen-Schillerh&ouml;he
                                                    <br>
                                                    <br>
                                                    <b>Board of management</b>
                                                    <br>Dr.&nbsp;Stefan&nbsp;Hartung, Dr.&nbsp;Christian&nbsp;Fischer, Filiz&nbsp;Albrecht, Dr.&nbsp;Markus&nbsp;Forschner, Dr.&nbsp;Markus&nbsp;Heyn, Rolf&nbsp;Najork                          
                                                </td>
                                                <td class="dyn-col" valign="top"
                                                    style="width: 50%; padding: 16px; font-size: 12px; line-height: 18px;">
                                                    <b>Registration court</b>
                                                    <br>
                                                    District court Stuttgart HRB 14000
                                                    <br>
                                                    <br>
                                                    <b>VAT identification number</b>
                                                    <br>
                                                    DE811128135
                                                    <br>
                                                    <br>
                                                    <b>Your contact at Bosch</b>
                                                    <br>
                                                    <a href="mailto:ITServiceDesk@bosch.com">
                                                        ITServiceDesk@bosch.com
                                                    </a>
                                                    <br>
                                                    +49 (711) 811-3311
                                                    <br>
                                                    <br>
                                                    <a href="https://www.bosch.de/datenschutzhinweise/?prevent-auto-open-privacy-settings=1">
                                                        Data privacy policy
                                                    </a>
                                                </td>
                                            </tr>
    
                                            <tr>
                                                <td colspan="2"
                                                    style="padding: 8px 16px 16px; background-color: #EFF1F2; font-size: 12px; font-style: italic; line-height: 18px;">
                                                    This is an automatically generated email. You are receiving it as member of the server used by.
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>
                            </table>
                        </body>
                    </html>
                    '''.format(host_used_by)

    # Windows SQL Server installation failed
    elif email_type == '6':
        if incident:
            email_msg['subject'] = '[' + str(
                incident) + '] Windows SQL Server installation failed for ' + host_name
        else:
            email_msg['subject'] = 'Windows SQL Server installation failed for ' + host_name
        email_msg['content'] = '''
                        <!DOCTYPE html>
                        <html lang="en">
                            <head>
                                <title>SQL Server installation failed</title>
                                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                                <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
                                <meta name="color-scheme" content="only">
                                <meta http-equiv="X-Render-Mode" content="html">
                                <style type="text/css">
                                    body {{font-size: 16px; line-height: 24px; font-family: Bosch Office Sans, Arial, sans-serif;}}
    
                                    a {{text-decoration: none; color: #007BC0;}}
    
                                    @media screen and (max-width: 640px) {{
                                        #innerTable {{width: 320px !important;}}
    
                                        #header-logo {{
                                            display: block !important;
                                            float: left !important;
                                            width: 100% !important;
                                        }}
    
                                        #header-text {{
                                            display: block !important;
                                            float: left !important;
                                            width: 100% !important;
                                            text-align: left !important;
                                            padding: 0px 0px 0px 16px !important;
                                        }}
    
                                        .dyn-col {{
                                            display: block !important;
                                            float: left !important;
                                            width: 100% !important;
                                            box-sizing: border-box !important;
                                        }}
                                    }}
    
                                    @supports (-webkit-touch-callout: none) {{
                                        body {{
                                            background-color: #EFF1F2;
                                        }}
                                    }}
                                </style>
                            </head>
    
                            <body style="margin: 0px;">
                                <table id="outerTable" cellpadding="0" cellspacing="0" border="0" style="width: 100%; background-color: #EFF1F2;">
                                    <tr>
                                        <td>
                                            <span
                                                style="color: #EFF1F2; display: none; opacity: 0; overflow: hidden; mso-hide: all; visibility: hidden;">
                                                Customer Notification - SQL Server installation failed<br>
                                                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                                            </span>
    
                                            <table id="innerTable" cellpadding="0" cellspacing="0" border="0" align="center" style="width: 640px; background-color: #FFF; margin-bottom: 16px;">
                                                <tr>
                                                    <td colspan="2" style="line-height: 0px;">
                                                        <img width="640" height="6" style="height: 6px; width: 100%;" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAABQAAAAAMCAMAAAAKwOAZAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAADwUExURZUkMp8kNLEnOa8gJMEhKtQgJ54vZn42hW03jWo4jWg4jmU5jmM5jmE6jl86jlw7jlk7j1c8j1M8j1A9j00+kEo+kEk/kEc/kEY/kERAkEJAkD9BkTxBkTo8gDc8gDU8fzM8fy89fiw9fSk9fSU+gyY8gig7gCo4hiNAhiVdoSZeoi9+tTmUwDijyzmjyzqkywWmywWetgqdXAqdXQqcXkGoZIm8blOuamKxbTKNRrAkMbIpTiM+hBClygWlywablB6iYjmfWzB+th2lyXu5bDKWULAiKy6kxweac2+2a4o1fQWlyidOljGNRjB/tgAAAJPcmuEAAABQdFJOU/////////////////////////////////////////////////////////////////////////////////////////////////////////8AE3OmeQAAAAlwSFlzAAAOwwAADsMBx2+oZAAABWBJREFUaEPd221v2lYYxvEpoQ30DXkZpIBIkICmhRCUjIx02bRm0oqWfv+Ps/vhOk9gE/v42HX3Pwfbadq3P9226S8NtD3pbKM+286p7V2ben929oGSw0Hn2LKwM7twGwt7r0HQ5aVuNBrOxmP+6D5o6q/DZvPcNa2y3m52vPnHFH2q1qKxVjV0t26oh18T9/BtQ+vhtwaCUXW2PYlvC/5OTzuwpxWdkHNZBLJ5WfxlKMjg2Y0VbC9x72JEH1qhf5eD2dA0HgI9L0+/8fRqcqV74pp/mWSv+RdpGrcKMAjp8gJh1QJksX0HT/X3O9BK2R/wKbL7oq3/hFvJ2jxSm79hVK0BqVoDZjG1FMB36l3mBOj4c0uyBCp79iKDQM4zkPzDGDgjAEMCB06/HAGvXEyfbjRl5ua85hO68D+kGJ2nymAMhHw4xiCgywuEVeuvan0GT7V32yIAwVqJ1nArWS8M4OP/BsCn+BmwpQA+feieCX/mozF2IiAMtOOffPZi8HTbhW1OtkviT6Y/NlDs80bAsS/gQVPQJzF9ukzWNxuRyCryL2gI5J+w5JellzKYGaDL698bIFalT5AssooA3hZvsVo9J271D0Qr1L2uqNbfAFeyeATcgKh6g1G1to0G0PnXroeA+ggwMyUwWLydgcqeHtw1FvZ+gxEryA6qfnn+ZRgI+6QD/zIA1GgEVLz4yv6Av21wK7R00zqYBAFdTvMU/v04AOFa4b5CrZSBtiLdyyG29A8BGcBGHgG2/BlgSwHs7GT+0yGQM2c7/Kl8OvvZ6c9eUI4/NU9O5hLbphPgTMbA/QnQAGj1CwkMJ0Ci75qWJ6CSlhP7J1OgEigbCJZhMDi5IF1OSQbAqrfA0KxMAK1sy+QD4HPhdyCsHyiLDW4lq7E74HY/A/T9axOA73e7roCnxyDBT/Uj8HDQc5jlTw+ysDWPQL715WaEYTgBDspMgIQf5wFoOTsePxQUwaxjfCGZn44s71IWH94GEIRVC5DFBtQKBckiW0CthBUEMPa+NwhuJYsfAkKomoNRtRb9DBD0acCnDe12O34ISINft2unP4qdw5EOPVr9fl8OHOBT8bwLoc8tt21y74sUPyvgyLwEtvwdmwDFPxLwGv4VFlAy/tktmuFX+cu7dIs2pMvpJwLwtiJ+3HJ1l3oGLPAOJAl+1PoFcCVr09AjwFY/AwwGwBa9BTkhADEBHoyAdgDs9XuEnx6QqGdT/tg8z0DKl882GOgbEL4F9ifAkXkJbG6Bj0yAkzH8IwFtRrCiCV269SwXfOb0em95l27RhnQ5EYAJboIBWWwQ7lgp9KP0ezB3zwn3mwBCrwTV8RCwmTvgNj8DDP1rEYB0B7w769II2KUIvV6vp/qxfXoU9ax8Jiuf5gi86Ct/9hAoOJPJT98C6/cAnYD2W4DiX8YEeH0N/6548jOBPwp0lU3pE8zMWa7lj8PlXQYL0uVEet1UrHYAE+HHLfgtiHx5JVnyYiM30JUquJUseQT42kBAqtYAWsm2bQWwQ/4RgDz/CYDknwGQ0ntfDH+cYxDuWfZ4D8/JvvOhAmgI1MwF86eP/waD0d4zwL0BUPALBCTswJ+b/6pMgGHyr4U4bPrIn+FKlr3YW5AupwQAEoGALLJj/xNkmQ4/arH4rPetCcsHEGilDG4l62XTCH+vjdwCd0Baufb8a89DwCcF0CQAqoB6/8v0iXrCoJ41+IdUQCJQ7WPvREDdhj9OCcTbYMHPCEjcIQB4cAtM8CmAQeCPAldV8gQ0BsqV/0PGgnQ5pfDv5uP3CuUDuFwuAVeqFouvqb8ImPcOBGKlbf0IuJL1AKHq7fX1P49vbnJ3XXkBAAAAAElFTkSuQmCC" />
                                                    </td>
                                                </tr>
    
                                                <tr>
                                                    <td colspan="2" style="height: 24px;"></td>
                                                </tr>
                                                <tr>
                                                    <td colspan="2">
                                                        <table cellpadding="0" cellspacing="0" border="0" style="width: 100%;">
                                                            <tr>
                                                                <td id="header-logo" valign="top" style="padding-left: 16px;">
                                                                    <img height="32" width="143" style="height: 32px; width: 143px;" src="data:image/png;base64,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" />
                                                                </td>
                                                                <td id="header-text" style="text-align: right; padding-right: 16px; mso-line-height-rule: exactly;">
                                                                    <p
                                                                        style="margin: 6px 0px; padding: 0px; font-size: 20px; line-height: 20px; font-weight: bold;">
                                                                        Customer Notification
                                                                    </p>
                                                                    <p style="margin: 2px 0px; padding: 0px; font-size: 14px; line-height: 14px;">
                                                                        BD Global Operation Center
                                                                    </p>
                                                                </td>
                                                            </tr>
                                                        </table>
                                                    </td>
                                                </tr>
    
                                                <tr>
                                                    <td colspan="2" style="padding: 54px 16px 0px;">
                                                        <h1 style="margin: 0px; font-size: 32px; line-height: 32px; font-weight: bold; text-align: center;">
                                                            SQL Server installation failed
                                                        </h1>
                                                    </td>
                                                </tr>
    
                                                <tr>
                                                    <td colspan="2" style="padding: 32px 16px 0px;">
                                                        Dear Customer,<br><br>For hardened servers it's not possible to install an MS-SQL server or MS-SQL Express. 
                                                        During the installation process the setup requires a lot of user privileges and after the hardening one of the required critical user privilege is not given.<br><br>
                                                        Please request the permanent exception ("enable debug programs") for <b>{}</b> via Hardening Exception self service:
                                                        <i><a href="https://rb-servicecatalog.apps.intranet.bosch.com/RequestCenter/website/Grunt/application/offer.html?id=4287">Server Hardening/ Security logging Exceptions<span style='font-style:normal'>.</span></a></i><br><br>
                                                        Then try to installed it by yourself, because software installation is server owner's responsibility.<br><br>
                                                        Thanks for your understanding and cooperation.<br>
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td colspan="2" style="height: 32px;"></td>
                                                </tr>
                                                <tr>
                                                    <td colspan="2" style="height: 1px; background-color: #E0E2E5;"></td>
                                                </tr>
                                                <tr>
                                                    <td class="dyn-col" valign="top"
                                                        style="width: 50%; padding: 16px; font-size: 12px; line-height: 18px;">
                                                        <b>Name and address</b>
                                                        <br>
                                                        Robert Bosch GmbH
                                                        <br>
                                                        Robert-Bosch-Platz 1
                                                        <br>
                                                        70839 Gerlingen-Schillerh&ouml;he
                                                        <br>
                                                        <br>
                                                        <b>Board of management</b>
                                                        <br>Dr.&nbsp;Stefan&nbsp;Hartung, Dr.&nbsp;Christian&nbsp;Fischer, Filiz&nbsp;Albrecht, Dr.&nbsp;Markus&nbsp;Forschner, Dr.&nbsp;Markus&nbsp;Heyn, Rolf&nbsp;Najork                          
                                                    </td>
                                                    <td class="dyn-col" valign="top"
                                                        style="width: 50%; padding: 16px; font-size: 12px; line-height: 18px;">
                                                        <b>Registration court</b>
                                                        <br>
                                                        District court Stuttgart HRB 14000
                                                        <br>
                                                        <br>
                                                        <b>VAT identification number</b>
                                                        <br>
                                                        DE811128135
                                                        <br>
                                                        <br>
                                                        <b>Your contact at Bosch</b>
                                                        <br>
                                                        <a href="mailto:ITServiceDesk@bosch.com">
                                                            ITServiceDesk@bosch.com
                                                        </a>
                                                        <br>
                                                        +49 (711) 811-3311
                                                        <br>
                                                        <br>
                                                        <a href="https://www.bosch.de/datenschutzhinweise/?prevent-auto-open-privacy-settings=1">
                                                            Data privacy policy
                                                        </a>
                                                    </td>
                                                </tr>
    
                                                <tr>
                                                    <td colspan="2"
                                                        style="padding: 8px 16px 16px; background-color: #EFF1F2; font-size: 12px; font-style: italic; line-height: 18px;">
                                                        This is an automatically generated email. You are receiving it as member of the server used by.
                                                    </td>
                                                </tr>
                                            </table>
                                        </td>
                                    </tr>
                                </table>
                            </body>
                        </html>
                        '''.format(host_name)

    # Server reinstallation for EV/MTP
    elif email_type == '7':
        if incident:
            email_msg['subject'] = '[' + str(
                incident) + '] Server Maintenance Notice: Issues Post System Recovery for ' + host_name
        else:
            email_msg['subject'] = 'Server Maintenance Notice: Issues Post System Recovery for ' + host_name
        email_msg['content'] = '''
                            <!DOCTYPE html>
                            <html lang="en">
                                <head>
                                    <title>SQL Server installation failed</title>
                                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                                    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
                                    <meta name="color-scheme" content="only">
                                    <meta http-equiv="X-Render-Mode" content="html">
                                    <style type="text/css">
                                        body {{font-size: 16px; line-height: 24px; font-family: Bosch Office Sans, Arial, sans-serif;}}
    
                                        a {{text-decoration: none; color: #007BC0;}}
    
                                        @media screen and (max-width: 640px) {{
                                            #innerTable {{width: 320px !important;}}
    
                                            #header-logo {{
                                                display: block !important;
                                                float: left !important;
                                                width: 100% !important;
                                            }}
    
                                            #header-text {{
                                                display: block !important;
                                                float: left !important;
                                                width: 100% !important;
                                                text-align: left !important;
                                                padding: 0px 0px 0px 16px !important;
                                            }}
    
                                            .dyn-col {{
                                                display: block !important;
                                                float: left !important;
                                                width: 100% !important;
                                                box-sizing: border-box !important;
                                            }}
                                        }}
    
                                        @supports (-webkit-touch-callout: none) {{
                                            body {{
                                                background-color: #EFF1F2;
                                            }}
                                        }}
                                    </style>
                                </head>
    
                                <body style="margin: 0px;">
                                    <table id="outerTable" cellpadding="0" cellspacing="0" border="0" style="width: 100%; background-color: #EFF1F2;">
                                        <tr>
                                            <td>
                                                <span
                                                    style="color: #EFF1F2; display: none; opacity: 0; overflow: hidden; mso-hide: all; visibility: hidden;">
                                                    Customer Notification - Issues Post System Recovery<br>
                                                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                                                </span>
    
                                                <table id="innerTable" cellpadding="0" cellspacing="0" border="0" align="center" style="width: 640px; background-color: #FFF; margin-bottom: 16px;">
                                                    <tr>
                                                        <td colspan="2" style="line-height: 0px;">
                                                            <img width="640" height="6" style="height: 6px; width: 100%;" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAABQAAAAAMCAMAAAAKwOAZAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAADwUExURZUkMp8kNLEnOa8gJMEhKtQgJ54vZn42hW03jWo4jWg4jmU5jmM5jmE6jl86jlw7jlk7j1c8j1M8j1A9j00+kEo+kEk/kEc/kEY/kERAkEJAkD9BkTxBkTo8gDc8gDU8fzM8fy89fiw9fSk9fSU+gyY8gig7gCo4hiNAhiVdoSZeoi9+tTmUwDijyzmjyzqkywWmywWetgqdXAqdXQqcXkGoZIm8blOuamKxbTKNRrAkMbIpTiM+hBClygWlywablB6iYjmfWzB+th2lyXu5bDKWULAiKy6kxweac2+2a4o1fQWlyidOljGNRjB/tgAAAJPcmuEAAABQdFJOU/////////////////////////////////////////////////////////////////////////////////////////////////////////8AE3OmeQAAAAlwSFlzAAAOwwAADsMBx2+oZAAABWBJREFUaEPd221v2lYYxvEpoQ30DXkZpIBIkICmhRCUjIx02bRm0oqWfv+Ps/vhOk9gE/v42HX3Pwfbadq3P9226S8NtD3pbKM+286p7V2ben929oGSw0Hn2LKwM7twGwt7r0HQ5aVuNBrOxmP+6D5o6q/DZvPcNa2y3m52vPnHFH2q1qKxVjV0t26oh18T9/BtQ+vhtwaCUXW2PYlvC/5OTzuwpxWdkHNZBLJ5WfxlKMjg2Y0VbC9x72JEH1qhf5eD2dA0HgI9L0+/8fRqcqV74pp/mWSv+RdpGrcKMAjp8gJh1QJksX0HT/X3O9BK2R/wKbL7oq3/hFvJ2jxSm79hVK0BqVoDZjG1FMB36l3mBOj4c0uyBCp79iKDQM4zkPzDGDgjAEMCB06/HAGvXEyfbjRl5ua85hO68D+kGJ2nymAMhHw4xiCgywuEVeuvan0GT7V32yIAwVqJ1nArWS8M4OP/BsCn+BmwpQA+feieCX/mozF2IiAMtOOffPZi8HTbhW1OtkviT6Y/NlDs80bAsS/gQVPQJzF9ukzWNxuRyCryL2gI5J+w5JellzKYGaDL698bIFalT5AssooA3hZvsVo9J271D0Qr1L2uqNbfAFeyeATcgKh6g1G1to0G0PnXroeA+ggwMyUwWLydgcqeHtw1FvZ+gxEryA6qfnn+ZRgI+6QD/zIA1GgEVLz4yv6Av21wK7R00zqYBAFdTvMU/v04AOFa4b5CrZSBtiLdyyG29A8BGcBGHgG2/BlgSwHs7GT+0yGQM2c7/Kl8OvvZ6c9eUI4/NU9O5hLbphPgTMbA/QnQAGj1CwkMJ0Ci75qWJ6CSlhP7J1OgEigbCJZhMDi5IF1OSQbAqrfA0KxMAK1sy+QD4HPhdyCsHyiLDW4lq7E74HY/A/T9axOA73e7roCnxyDBT/Uj8HDQc5jlTw+ysDWPQL715WaEYTgBDspMgIQf5wFoOTsePxQUwaxjfCGZn44s71IWH94GEIRVC5DFBtQKBckiW0CthBUEMPa+NwhuJYsfAkKomoNRtRb9DBD0acCnDe12O34ISINft2unP4qdw5EOPVr9fl8OHOBT8bwLoc8tt21y74sUPyvgyLwEtvwdmwDFPxLwGv4VFlAy/tktmuFX+cu7dIs2pMvpJwLwtiJ+3HJ1l3oGLPAOJAl+1PoFcCVr09AjwFY/AwwGwBa9BTkhADEBHoyAdgDs9XuEnx6QqGdT/tg8z0DKl882GOgbEL4F9ifAkXkJbG6Bj0yAkzH8IwFtRrCiCV269SwXfOb0em95l27RhnQ5EYAJboIBWWwQ7lgp9KP0ezB3zwn3mwBCrwTV8RCwmTvgNj8DDP1rEYB0B7w769II2KUIvV6vp/qxfXoU9ax8Jiuf5gi86Ct/9hAoOJPJT98C6/cAnYD2W4DiX8YEeH0N/6548jOBPwp0lU3pE8zMWa7lj8PlXQYL0uVEet1UrHYAE+HHLfgtiHx5JVnyYiM30JUquJUseQT42kBAqtYAWsm2bQWwQ/4RgDz/CYDknwGQ0ntfDH+cYxDuWfZ4D8/JvvOhAmgI1MwF86eP/waD0d4zwL0BUPALBCTswJ+b/6pMgGHyr4U4bPrIn+FKlr3YW5AupwQAEoGALLJj/xNkmQ4/arH4rPetCcsHEGilDG4l62XTCH+vjdwCd0Baufb8a89DwCcF0CQAqoB6/8v0iXrCoJ41+IdUQCJQ7WPvREDdhj9OCcTbYMHPCEjcIQB4cAtM8CmAQeCPAldV8gQ0BsqV/0PGgnQ5pfDv5uP3CuUDuFwuAVeqFouvqb8ImPcOBGKlbf0IuJL1AKHq7fX1P49vbnJ3XXkBAAAAAElFTkSuQmCC" />
                                                        </td>
                                                    </tr>
    
                                                    <tr>
                                                        <td colspan="2" style="height: 24px;"></td>
                                                    </tr>
                                                    <tr>
                                                        <td colspan="2">
                                                            <table cellpadding="0" cellspacing="0" border="0" style="width: 100%;">
                                                                <tr>
                                                                    <td id="header-logo" valign="top" style="padding-left: 16px;">
                                                                        <img height="32" width="143" style="height: 32px; width: 143px;" src="data:image/png;base64,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" />
                                                                    </td>
                                                                    <td id="header-text" style="text-align: right; padding-right: 16px; mso-line-height-rule: exactly;">
                                                                        <p
                                                                            style="margin: 6px 0px; padding: 0px; font-size: 20px; line-height: 20px; font-weight: bold;">
                                                                            Customer Notification
                                                                        </p>
                                                                        <p style="margin: 2px 0px; padding: 0px; font-size: 14px; line-height: 14px;">
                                                                            BD Global Operation Center
                                                                        </p>
                                                                    </td>
                                                                </tr>
                                                            </table>
                                                        </td>
                                                    </tr>
    
                                                    <tr>
                                                        <td colspan="2" style="padding: 54px 16px 0px;">
                                                            <h1 style="margin: 0px; font-size: 32px; line-height: 32px; font-weight: bold; text-align: center;">
                                                                Server Maintenance Notice: Issues Post System Recovery
                                                            </h1>
                                                        </td>
                                                    </tr>
    
                                                    <tr>
                                                        <td colspan="2" style="padding: 32px 16px 0px;">
                                                            Dear System Owners,<br><br>Thank you for your continued trust and support for Server Operations Center.<br>
                                                            I would like to bring to your attention some issues regarding your server {} that arose during the system recovery after the last EV site crash.<br><br>
                                                            Upon inspection, we have identified that certain Windows components have been damaged, which may impact the security performance of the server and potentially lead to unknown issues.<br><br>
                                                            Despite our attempts to manually repair, unfortunately, they were unsuccessful.To ensure the stability of your server, We strongly recommend reinstalling the operating system as soon as possible.<br>
                                                            You could trigger a reinstall procedure via the link: <i><a href="https://rb-servicecatalog.apps.intranet.bosch.com/RequestCenter/website/Grunt/application/offer.html?id=4523">Server Hosting - Server Reinstallation<span style='font-style:normal'>.</span></a></i><br><br>
                                                            Rest assured, reinstalling the system will not affect data on non-system drives; your files and data will be preserved. This step is crucial to ensure the smooth operation of the server and mitigate potential security risks.<br><br>
                                                            Thanks for your understanding and cooperation.<br>
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td colspan="2" style="height: 32px;"></td>
                                                    </tr>
                                                    <tr>
                                                        <td colspan="2" style="height: 1px; background-color: #E0E2E5;"></td>
                                                    </tr>
                                                    <tr>
                                                        <td class="dyn-col" valign="top"
                                                            style="width: 50%; padding: 16px; font-size: 12px; line-height: 18px;">
                                                            <b>Name and address</b>
                                                            <br>
                                                            Robert Bosch GmbH
                                                            <br>
                                                            Robert-Bosch-Platz 1
                                                            <br>
                                                            70839 Gerlingen-Schillerh&ouml;he
                                                            <br>
                                                            <br>
                                                            <b>Board of management</b>
                                                            <br>Dr.&nbsp;Stefan&nbsp;Hartung, Dr.&nbsp;Christian&nbsp;Fischer, Filiz&nbsp;Albrecht, Dr.&nbsp;Markus&nbsp;Forschner, Dr.&nbsp;Markus&nbsp;Heyn, Rolf&nbsp;Najork                          
                                                        </td>
                                                        <td class="dyn-col" valign="top"
                                                            style="width: 50%; padding: 16px; font-size: 12px; line-height: 18px;">
                                                            <b>Registration court</b>
                                                            <br>
                                                            District court Stuttgart HRB 14000
                                                            <br>
                                                            <br>
                                                            <b>VAT identification number</b>
                                                            <br>
                                                            DE811128135
                                                            <br>
                                                            <br>
                                                            <b>Your contact at Bosch</b>
                                                            <br>
                                                            <a href="mailto:ITServiceDesk@bosch.com">
                                                                ITServiceDesk@bosch.com
                                                            </a>
                                                            <br>
                                                            +49 (711) 811-3311
                                                            <br>
                                                            <br>
                                                            <a href="https://www.bosch.de/datenschutzhinweise/?prevent-auto-open-privacy-settings=1">
                                                                Data privacy policy
                                                            </a>
                                                        </td>
                                                    </tr>
    
                                                    <tr>
                                                        <td colspan="2"
                                                            style="padding: 8px 16px 16px; background-color: #EFF1F2; font-size: 12px; font-style: italic; line-height: 18px;">
                                                            This is an automatically generated email. You are receiving it as member of the server used by.
                                                        </td>
                                                    </tr>
                                                </table>
                                            </td>
                                        </tr>
                                    </table>
                                </body>
                            </html>
                            '''.format(host_name)

    return email_msg


def get_pmc_notification_msg(three_days_pmc_data):

    table_html = '''
        <table style="font-family: verdana,arial,sans-serif; font-size:11px; color:#333333; border-width: 1px; border-color: #666666; border-collapse: collapse;" cellspacing="1" border="1">
            <thead>
                <tr>
                    <th style="padding:8px;background-color: #dedede;">ITSP NO</th>
                    <th style="padding:8px;background-color: #dedede;">Change ID</th>
                    <th style="padding:8px;background-color: #dedede;">Status</th>
                    <th style="padding:8px;background-color: #dedede;">Region</th>
                    <th style="padding:8px;background-color: #dedede;">End Time</th>
                <tr>
            </thead>
            <tbody style="font-size:12px;">
    '''

    for pmc_data in three_days_pmc_data:
        table_html += '<tr>'
        table_html += '<td style="padding:8px">' + str(pmc_data[0]) + '</td>'
        table_html += '<td style="padding:8px">' + str(pmc_data[1]) + '</td>'
        table_html += '<td style="padding:8px">' + str(pmc_data[2]) + '</td>'
        table_html += '<td style="padding:8px">' + str(pmc_data[3]) + '</td>'
        table_html += '<td style="padding:8px">' + str(pmc_data[4]) + '</td>'
        table_html += '</tr>'

    table_html += '''
        </tbody>
	</table>
    '''

    email_msg_content = '''
                <!DOCTYPE html>
                <html lang="en">
                    <head>
                        <title>PMC Tool Notification - Activity Status Update</title>
                        <meta name="viewport" content="width=device-width, initial-scale=1.0">
                        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
                        <meta name="color-scheme" content="only">
                        <meta http-equiv="X-Render-Mode" content="html">
                        <style type="text/css">
                            body {{font-size: 16px; line-height: 24px; font-family: Bosch Office Sans, Arial, sans-serif;}}

                            a {{text-decoration: none; color: #007BC0;}}

                            @media screen and (max-width: 640px) {{
                                #innerTable {{width: 320px !important;}}

                                #header-logo {{
                                    display: block !important;
                                    float: left !important;
                                    width: 100% !important;
                                }}

                                #header-text {{
                                    display: block !important;
                                    float: left !important;
                                    width: 100% !important;
                                    text-align: left !important;
                                    padding: 0px 0px 0px 16px !important;
                                }}

                                .dyn-col {{
                                    display: block !important;
                                    float: left !important;
                                    width: 100% !important;
                                    box-sizing: border-box !important;
                                }}
                            }}

                            @supports (-webkit-touch-callout: none) {{
                                body {{
                                    background-color: #EFF1F2;
                                }}
                            }}
                        </style>
                    </head>

                    <body style="margin: 0px;">
                        <table id="outerTable" cellpadding="0" cellspacing="0" border="0" style="width: 100%; background-color: #EFF1F2;">
                            <tr>
                                <td>
                                    <span
                                        style="color: #EFF1F2; display: none; opacity: 0; overflow: hidden; mso-hide: all; visibility: hidden;">
                                        PMC Tool Notification - Activity Status Update<br>
                                        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                                    </span>

                                    <table id="innerTable" cellpadding="0" cellspacing="0" border="0" align="center" style="width: 640px; background-color: #FFF; margin-bottom: 16px;">
                                        <tr>
                                            <td colspan="2" style="line-height: 0px;">
                                                <img width="640" height="6" style="height: 6px; width: 100%;" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAABQAAAAAMCAMAAAAKwOAZAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAADwUExURZUkMp8kNLEnOa8gJMEhKtQgJ54vZn42hW03jWo4jWg4jmU5jmM5jmE6jl86jlw7jlk7j1c8j1M8j1A9j00+kEo+kEk/kEc/kEY/kERAkEJAkD9BkTxBkTo8gDc8gDU8fzM8fy89fiw9fSk9fSU+gyY8gig7gCo4hiNAhiVdoSZeoi9+tTmUwDijyzmjyzqkywWmywWetgqdXAqdXQqcXkGoZIm8blOuamKxbTKNRrAkMbIpTiM+hBClygWlywablB6iYjmfWzB+th2lyXu5bDKWULAiKy6kxweac2+2a4o1fQWlyidOljGNRjB/tgAAAJPcmuEAAABQdFJOU/////////////////////////////////////////////////////////////////////////////////////////////////////////8AE3OmeQAAAAlwSFlzAAAOwwAADsMBx2+oZAAABWBJREFUaEPd221v2lYYxvEpoQ30DXkZpIBIkICmhRCUjIx02bRm0oqWfv+Ps/vhOk9gE/v42HX3Pwfbadq3P9226S8NtD3pbKM+286p7V2ben929oGSw0Hn2LKwM7twGwt7r0HQ5aVuNBrOxmP+6D5o6q/DZvPcNa2y3m52vPnHFH2q1qKxVjV0t26oh18T9/BtQ+vhtwaCUXW2PYlvC/5OTzuwpxWdkHNZBLJ5WfxlKMjg2Y0VbC9x72JEH1qhf5eD2dA0HgI9L0+/8fRqcqV74pp/mWSv+RdpGrcKMAjp8gJh1QJksX0HT/X3O9BK2R/wKbL7oq3/hFvJ2jxSm79hVK0BqVoDZjG1FMB36l3mBOj4c0uyBCp79iKDQM4zkPzDGDgjAEMCB06/HAGvXEyfbjRl5ua85hO68D+kGJ2nymAMhHw4xiCgywuEVeuvan0GT7V32yIAwVqJ1nArWS8M4OP/BsCn+BmwpQA+feieCX/mozF2IiAMtOOffPZi8HTbhW1OtkviT6Y/NlDs80bAsS/gQVPQJzF9ukzWNxuRyCryL2gI5J+w5JellzKYGaDL698bIFalT5AssooA3hZvsVo9J271D0Qr1L2uqNbfAFeyeATcgKh6g1G1to0G0PnXroeA+ggwMyUwWLydgcqeHtw1FvZ+gxEryA6qfnn+ZRgI+6QD/zIA1GgEVLz4yv6Av21wK7R00zqYBAFdTvMU/v04AOFa4b5CrZSBtiLdyyG29A8BGcBGHgG2/BlgSwHs7GT+0yGQM2c7/Kl8OvvZ6c9eUI4/NU9O5hLbphPgTMbA/QnQAGj1CwkMJ0Ci75qWJ6CSlhP7J1OgEigbCJZhMDi5IF1OSQbAqrfA0KxMAK1sy+QD4HPhdyCsHyiLDW4lq7E74HY/A/T9axOA73e7roCnxyDBT/Uj8HDQc5jlTw+ysDWPQL715WaEYTgBDspMgIQf5wFoOTsePxQUwaxjfCGZn44s71IWH94GEIRVC5DFBtQKBckiW0CthBUEMPa+NwhuJYsfAkKomoNRtRb9DBD0acCnDe12O34ISINft2unP4qdw5EOPVr9fl8OHOBT8bwLoc8tt21y74sUPyvgyLwEtvwdmwDFPxLwGv4VFlAy/tktmuFX+cu7dIs2pMvpJwLwtiJ+3HJ1l3oGLPAOJAl+1PoFcCVr09AjwFY/AwwGwBa9BTkhADEBHoyAdgDs9XuEnx6QqGdT/tg8z0DKl882GOgbEL4F9ifAkXkJbG6Bj0yAkzH8IwFtRrCiCV269SwXfOb0em95l27RhnQ5EYAJboIBWWwQ7lgp9KP0ezB3zwn3mwBCrwTV8RCwmTvgNj8DDP1rEYB0B7w769II2KUIvV6vp/qxfXoU9ax8Jiuf5gi86Ct/9hAoOJPJT98C6/cAnYD2W4DiX8YEeH0N/6548jOBPwp0lU3pE8zMWa7lj8PlXQYL0uVEet1UrHYAE+HHLfgtiHx5JVnyYiM30JUquJUseQT42kBAqtYAWsm2bQWwQ/4RgDz/CYDknwGQ0ntfDH+cYxDuWfZ4D8/JvvOhAmgI1MwF86eP/waD0d4zwL0BUPALBCTswJ+b/6pMgGHyr4U4bPrIn+FKlr3YW5AupwQAEoGALLJj/xNkmQ4/arH4rPetCcsHEGilDG4l62XTCH+vjdwCd0Baufb8a89DwCcF0CQAqoB6/8v0iXrCoJ41+IdUQCJQ7WPvREDdhj9OCcTbYMHPCEjcIQB4cAtM8CmAQeCPAldV8gQ0BsqV/0PGgnQ5pfDv5uP3CuUDuFwuAVeqFouvqb8ImPcOBGKlbf0IuJL1AKHq7fX1P49vbnJ3XXkBAAAAAElFTkSuQmCC" />
                                            </td>
                                        </tr>

                                        <tr>
                                            <td colspan="2" style="height: 24px;"></td>
                                        </tr>
                                        <tr>
                                            <td colspan="2">
                                                <table cellpadding="0" cellspacing="0" border="0" style="width: 100%;">
                                                    <tr>
                                                        <td id="header-logo" valign="top" style="padding-left: 16px;">
                                                            <img height="32" width="143" style="height: 32px; width: 143px;" src="data:image/png;base64,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" />
                                                        </td>
                                                        <td id="header-text" style="text-align: right; padding-right: 16px; mso-line-height-rule: exactly;">
                                                            <p
                                                                style="margin: 6px 0px; padding: 0px; font-size: 20px; line-height: 20px; font-weight: bold;">
                                                                PMC Tool Notification
                                                            </p>
                                                            <p style="margin: 2px 0px; padding: 0px; font-size: 14px; line-height: 14px;">
                                                                BD Global Operation Center
                                                            </p>
                                                        </td>
                                                    </tr>
                                                </table>
                                            </td>
                                        </tr>

                                        <tr>
                                            <td colspan="2" style="padding: 54px 16px 0px;">
                                                <h1 style="margin: 0px; font-size: 32px; line-height: 32px; font-weight: bold; text-align: center;">
                                                    PMC Activity Status Update
                                                </h1>
                                            </td>
                                        </tr>

                                        <tr>
                                            <td colspan="2" style="padding: 32px 16px 0px;">
                                                Dear Coordinator,<br><br>Your PMC activity plan as below already exceeded end time, please check the activity status and take action.<br><br>
                                                {}
                                            </td>
                                        </tr>
                                        <tr>
                                            <td colspan="2" style="height: 32px;"></td>
                                        </tr>
                                        <tr>
                                            <td colspan="2" style="height: 1px; background-color: #E0E2E5;"></td>
                                        </tr>
                                        <tr>
                                            <td class="dyn-col" valign="top"
                                                style="width: 50%; padding: 16px; font-size: 12px; line-height: 18px;">
                                                <b>Name and address</b>
                                                <br>
                                                Robert Bosch GmbH
                                                <br>
                                                Robert-Bosch-Platz 1
                                                <br>
                                                70839 Gerlingen-Schillerh&ouml;he
                                                <br>
                                                <br>
                                                <b>Board of management</b>
                                                <br>Dr.&nbsp;Stefan&nbsp;Hartung, Dr.&nbsp;Christian&nbsp;Fischer, Filiz&nbsp;Albrecht, Dr.&nbsp;Markus&nbsp;Forschner, Dr.&nbsp;Markus&nbsp;Heyn, Rolf&nbsp;Najork                          
                                            </td>
                                            <td class="dyn-col" valign="top"
                                                style="width: 50%; padding: 16px; font-size: 12px; line-height: 18px;">
                                                <b>Registration court</b>
                                                <br>
                                                District court Stuttgart HRB 14000
                                                <br>
                                                <br>
                                                <b>VAT identification number</b>
                                                <br>
                                                DE811128135
                                                <br>
                                                <br>
                                                <b>Your contact at Bosch</b>
                                                <br>
                                                <a href="mailto:ITServiceDesk@bosch.com">
                                                    ITServiceDesk@bosch.com
                                                </a>
                                                <br>
                                                +49 (711) 811-3311
                                                <br>
                                                <br>
                                                <a href="https://www.bosch.de/datenschutzhinweise/?prevent-auto-open-privacy-settings=1">
                                                    Data privacy policy
                                                </a>
                                            </td>
                                        </tr>

                                        <tr>
                                            <td colspan="2"
                                                style="padding: 8px 16px 16px; background-color: #EFF1F2; font-size: 12px; font-style: italic; line-height: 18px;">
                                                This is an automatically generated email. You are receiving it as member of the PMC coordinator.
                                            </td>
                                        </tr>
                                    </table>
                                </td>
                            </tr>
                        </table>
                    </body>
                </html>
                '''.format(table_html)

    return email_msg_content


def get_disk_utilization_notification(host_name, disk_size_list):

    email_msg = {'subject':'', 'content':''}

    email_msg['subject'] = '[' + host_name + '] Disk C: free space decreased, please clean up or extend'

    email_msg['content'] = '''
            <!DOCTYPE html>
            <html lang="en">
                <head>
                    <title>Disk C: free space decreased</title>
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
                    <meta name="color-scheme" content="only">
                    <meta http-equiv="X-Render-Mode" content="html">
                    <style type="text/css">
                        body {{font-size: 16px; line-height: 24px; font-family: Bosch Office Sans, Arial, sans-serif;}}
    
                        a {{text-decoration: none; color: #007BC0;}}
    
                        @media screen and (max-width: 640px) {{
                            #innerTable {{width: 320px !important;}}
    
                            #header-logo {{
                                display: block !important;
                                float: left !important;
                                width: 100% !important;
                            }}
    
                            #header-text {{
                                display: block !important;
                                float: left !important;
                                width: 100% !important;
                                text-align: left !important;
                                padding: 0px 0px 0px 16px !important;
                            }}
    
                            .dyn-col {{
                                display: block !important;
                                float: left !important;
                                width: 100% !important;
                                box-sizing: border-box !important;
                            }}
                        }}
    
                        @supports (-webkit-touch-callout: none) {{
                            body {{
                                background-color: #EFF1F2;
                            }}
                        }}
                    </style>
                </head>
    
                <body style="margin: 0px;">
                    <table id="outerTable" cellpadding="0" cellspacing="0" border="0" style="width: 100%; background-color: #EFF1F2;">
                        <tr>
                            <td>
                                <span
                                    style="color: #EFF1F2; display: none; opacity: 0; overflow: hidden; mso-hide: all; visibility: hidden;">
                                    Customer Notification - Disk C: free space decreased<br>
                                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                                </span>
    
                                <table id="innerTable" cellpadding="0" cellspacing="0" border="0" align="center" style="width: 640px; background-color: #FFF; margin-bottom: 16px;">
                                    <tr>
                                        <td colspan="2" style="line-height: 0px;">
                                            <img width="640" height="6" style="height: 6px; width: 100%;" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAABQAAAAAMCAMAAAAKwOAZAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAADwUExURZUkMp8kNLEnOa8gJMEhKtQgJ54vZn42hW03jWo4jWg4jmU5jmM5jmE6jl86jlw7jlk7j1c8j1M8j1A9j00+kEo+kEk/kEc/kEY/kERAkEJAkD9BkTxBkTo8gDc8gDU8fzM8fy89fiw9fSk9fSU+gyY8gig7gCo4hiNAhiVdoSZeoi9+tTmUwDijyzmjyzqkywWmywWetgqdXAqdXQqcXkGoZIm8blOuamKxbTKNRrAkMbIpTiM+hBClygWlywablB6iYjmfWzB+th2lyXu5bDKWULAiKy6kxweac2+2a4o1fQWlyidOljGNRjB/tgAAAJPcmuEAAABQdFJOU/////////////////////////////////////////////////////////////////////////////////////////////////////////8AE3OmeQAAAAlwSFlzAAAOwwAADsMBx2+oZAAABWBJREFUaEPd221v2lYYxvEpoQ30DXkZpIBIkICmhRCUjIx02bRm0oqWfv+Ps/vhOk9gE/v42HX3Pwfbadq3P9226S8NtD3pbKM+286p7V2ben929oGSw0Hn2LKwM7twGwt7r0HQ5aVuNBrOxmP+6D5o6q/DZvPcNa2y3m52vPnHFH2q1qKxVjV0t26oh18T9/BtQ+vhtwaCUXW2PYlvC/5OTzuwpxWdkHNZBLJ5WfxlKMjg2Y0VbC9x72JEH1qhf5eD2dA0HgI9L0+/8fRqcqV74pp/mWSv+RdpGrcKMAjp8gJh1QJksX0HT/X3O9BK2R/wKbL7oq3/hFvJ2jxSm79hVK0BqVoDZjG1FMB36l3mBOj4c0uyBCp79iKDQM4zkPzDGDgjAEMCB06/HAGvXEyfbjRl5ua85hO68D+kGJ2nymAMhHw4xiCgywuEVeuvan0GT7V32yIAwVqJ1nArWS8M4OP/BsCn+BmwpQA+feieCX/mozF2IiAMtOOffPZi8HTbhW1OtkviT6Y/NlDs80bAsS/gQVPQJzF9ukzWNxuRyCryL2gI5J+w5JellzKYGaDL698bIFalT5AssooA3hZvsVo9J271D0Qr1L2uqNbfAFeyeATcgKh6g1G1to0G0PnXroeA+ggwMyUwWLydgcqeHtw1FvZ+gxEryA6qfnn+ZRgI+6QD/zIA1GgEVLz4yv6Av21wK7R00zqYBAFdTvMU/v04AOFa4b5CrZSBtiLdyyG29A8BGcBGHgG2/BlgSwHs7GT+0yGQM2c7/Kl8OvvZ6c9eUI4/NU9O5hLbphPgTMbA/QnQAGj1CwkMJ0Ci75qWJ6CSlhP7J1OgEigbCJZhMDi5IF1OSQbAqrfA0KxMAK1sy+QD4HPhdyCsHyiLDW4lq7E74HY/A/T9axOA73e7roCnxyDBT/Uj8HDQc5jlTw+ysDWPQL715WaEYTgBDspMgIQf5wFoOTsePxQUwaxjfCGZn44s71IWH94GEIRVC5DFBtQKBckiW0CthBUEMPa+NwhuJYsfAkKomoNRtRb9DBD0acCnDe12O34ISINft2unP4qdw5EOPVr9fl8OHOBT8bwLoc8tt21y74sUPyvgyLwEtvwdmwDFPxLwGv4VFlAy/tktmuFX+cu7dIs2pMvpJwLwtiJ+3HJ1l3oGLPAOJAl+1PoFcCVr09AjwFY/AwwGwBa9BTkhADEBHoyAdgDs9XuEnx6QqGdT/tg8z0DKl882GOgbEL4F9ifAkXkJbG6Bj0yAkzH8IwFtRrCiCV269SwXfOb0em95l27RhnQ5EYAJboIBWWwQ7lgp9KP0ezB3zwn3mwBCrwTV8RCwmTvgNj8DDP1rEYB0B7w769II2KUIvV6vp/qxfXoU9ax8Jiuf5gi86Ct/9hAoOJPJT98C6/cAnYD2W4DiX8YEeH0N/6548jOBPwp0lU3pE8zMWa7lj8PlXQYL0uVEet1UrHYAE+HHLfgtiHx5JVnyYiM30JUquJUseQT42kBAqtYAWsm2bQWwQ/4RgDz/CYDknwGQ0ntfDH+cYxDuWfZ4D8/JvvOhAmgI1MwF86eP/waD0d4zwL0BUPALBCTswJ+b/6pMgGHyr4U4bPrIn+FKlr3YW5AupwQAEoGALLJj/xNkmQ4/arH4rPetCcsHEGilDG4l62XTCH+vjdwCd0Baufb8a89DwCcF0CQAqoB6/8v0iXrCoJ41+IdUQCJQ7WPvREDdhj9OCcTbYMHPCEjcIQB4cAtM8CmAQeCPAldV8gQ0BsqV/0PGgnQ5pfDv5uP3CuUDuFwuAVeqFouvqb8ImPcOBGKlbf0IuJL1AKHq7fX1P49vbnJ3XXkBAAAAAElFTkSuQmCC" />
                                        </td>
                                    </tr>
    
                                    <tr>
                                        <td colspan="2" style="height: 24px;"></td>
                                    </tr>
                                    <tr>
                                        <td colspan="2">
                                            <table cellpadding="0" cellspacing="0" border="0" style="width: 100%;">
                                                <tr>
                                                    <td id="header-logo" valign="top" style="padding-left: 16px;">
                                                        <img height="32" width="143" style="height: 32px; width: 143px;" src="data:image/png;base64,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" />
                                                    </td>
                                                    <td id="header-text" style="text-align: right; padding-right: 16px; mso-line-height-rule: exactly;">
                                                        <p
                                                            style="margin: 6px 0px; padding: 0px; font-size: 20px; line-height: 20px; font-weight: bold;">
                                                            Customer Notification
                                                        </p>
                                                        <p style="margin: 2px 0px; padding: 0px; font-size: 14px; line-height: 14px;">
                                                            BD Global Operation Center
                                                        </p>
                                                    </td>
                                                </tr>
                                            </table>
                                        </td>
                                    </tr>
                                    
                                    <tr>
                                        <td colspan="2" style="padding: 54px 16px 0px;">
                                            <h1 style="margin: 0px; font-size: 32px; line-height: 32px; font-weight: bold; text-align: center;">
                                                Disk C: free space decreased
                                            </h1>
                                        </td>
                                    </tr>
                                    
                                    <tr>
                                        <td colspan="2" style="padding: 32px 16px 0px;">
                                            Dear System Owner,<br><br>During the last four hours, we have monitored your server <b>{}</b> is having a disk performance issue.<br><br>
                                            Please make sure that there are no <b>application data</b> (including log files) is stored on Disk C. If this is the case, please move application data to other discs. <br>
                                            Please delete the data or move it to other drives in order not to jeopardize the stability of the operating system:<br><br>
                                            <pre>{}</pre>
                                            <br><br>
                                            If you need an additional data disk or enlarge the existing data disc, you can order this by the following ITSP Order Form: <i><a href="https://service-management.bosch.tech/sp?id=search_itsp&spa=1&t=rsc&q=Server%20Hosting%20%E2%80%93%20Server%20Change%20Request%20(Physical%20and%20Virtual)">Server Hosting – Server Change Request (Physical and Virtual)<span style='font-style:normal'>.</span></a></i><br><br>
                                            Thanks for your understanding.<br>
                                            BD-Server-Opeartion-Center will continuously monitor your server.<br><br><br>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td colspan="2" style="height: 32px;"></td>
                                    </tr>
                                    <tr>
                                        <td colspan="2" style="height: 1px; background-color: #E0E2E5;"></td>
                                    </tr>
                                    <tr>
                                        <td class="dyn-col" valign="top"
                                            style="width: 50%; padding: 16px; font-size: 12px; line-height: 18px;">
                                            <b>Name and address</b>
                                            <br>
                                            Robert Bosch GmbH
                                            <br>
                                            Robert-Bosch-Platz 1
                                            <br>
                                            70839 Gerlingen-Schillerh&ouml;he
                                            <br>
                                            <br>
                                            <b>Board of management</b>
                                            <br>Dr.&nbsp;Stefan&nbsp;Hartung, Dr.&nbsp;Christian&nbsp;Fischer, Filiz&nbsp;Albrecht, Dr.&nbsp;Markus&nbsp;Forschner, Dr.&nbsp;Markus&nbsp;Heyn, Rolf&nbsp;Najork                          
                                        </td>
                                        <td class="dyn-col" valign="top"
                                            style="width: 50%; padding: 16px; font-size: 12px; line-height: 18px;">
                                            <b>Registration court</b>
                                            <br>
                                            District court Stuttgart HRB 14000
                                            <br>
                                            <br>
                                            <b>VAT identification number</b>
                                            <br>
                                            DE811128135
                                            <br>
                                            <br>
                                            <b>Your contact at Bosch</b>
                                            <br>
                                            <a href="mailto:ITServiceDesk@bosch.com">
                                                ITServiceDesk@bosch.com
                                            </a>
                                            <br>
                                            +49 (711) 811-3311
                                            <br>
                                            <br>
                                            <a href="https://www.bosch.de/datenschutzhinweise/?prevent-auto-open-privacy-settings=1">
                                                Data privacy policy
                                            </a>
                                        </td>
                                    </tr>
    
                                    <tr>
                                        <td colspan="2"
                                            style="padding: 8px 16px 16px; background-color: #EFF1F2; font-size: 12px; font-style: italic; line-height: 18px;">
                                            This is an automatically generated email. You are receiving it as member of the server used by.
                                        </td>
                                    </tr>
                                </table>
                            </td>
                        </tr>
                    </table>
                </body>
            </html>
            '''.format(host_name, disk_size_list.replace('\\n', '<br>'))
    
    return email_msg
