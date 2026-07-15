"""create_all()이 모든 테이블을 인식하도록 Base와 모델을 한곳에 모아둔다."""

from app.db.base_class import Base  # noqa: F401
from app.models.district import District  # noqa: F401
from app.models.place import Place  # noqa: F401
from app.models.place_type import PlaceType  # noqa: F401
from app.models.post import Post  # noqa: F401
from app.models.post_category import PostCategory  # noqa: F401
from app.models.post_place import post_place  # noqa: F401
