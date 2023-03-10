from sqlalchemy.orm import Session

from config import engine
from experimental.api import app
from experimental.sources import get_source_service, get_source_parser


@app.route('/sources/<source_name>', methods=['GET'])
def show(source_name: str):
    service = get_source_service(source_name)

    with Session(engine) as session:
        items = service.list(session)
        serialized_items = [item.as_dict() for item in items]
        return serialized_items


@app.route('/sources/<source_name>/parse', methods=['GET'])
def parse(source_name: str):
    service = get_source_service(source_name)

    parser = get_source_parser(source_name)
    with Session(engine) as session:
        [service.create(session, item) for item in parser.parse_items()]
        session.commit()

    return 'All items have been parsed'
