from check_in.connection import get_connection
from check_in.session import Session

db_session = Session(get_connection())
db_session.log_on_insertion()
db_session.delete_log_procedure()