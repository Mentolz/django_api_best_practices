from django.shortcuts import get_object_or_404
from rest_framework.response import Response

class BookModel:
    uid = models.Charfield()
    title = models.Charfield()
    author = models.Charfield()

# I used a model to DRY the Book json interface allowing me to reuse-it
# through all apis. You shoul'd be carefull when to use this because it
# can have unwanted side effects if you change the father class without
# intendind to change in some apis that it's being used
class BookSerializer:
    uid = serializers.Charfield()
    title = serializers.Charfield()
    author = serializers.Charfield()


class BooksAPI:
    class InputSerializer:
        title = serializers.Charfield()
        author = serializers.Charfield(required=False)

    class OutputSerializer:
        detail = BookSerializer(source="*")
        detail_url = serializers.MethodField()

        def get_detail_url(self, obj) -> str:
            # this is a simple solution that works fine to build an url.
            # It may be easier to build an url this way ratter than using a
            # class field.
            return reverse("core:books-detail", args=[obj.uid])

    def post(self, request, *args, **kwargs):
        """This API have 3 responsabilities:
        - knows who needs to call to validate data
        - knows what services needs to call to make the desired operation
        - knows who needs to call to build the response and returns it
        """
        # ------------------------- validates data ------------------------- #
        serializer = self.InputSerializer(request.data)
        serializer.is_valid(raise_exception=True)
        # validates data or sends http 400 response for free.

        # ------- call services to acomplish the desired operation  -------- #
        book: BookModel = services.create_book(
            title=serializer.validated_data["title"], 
            # enforce invariant that title is required
            author=serializer.validated_data.get("author")
            # deals gracefully with invariant that author is non required.
        )

        # ---------------- build the response and return it ---------------- #
        return Response(data=self.BookSerializer(book).data)

class BooksDetailApi:
    def get(self, request, uid: str, *args, **kwargs):
        """This API have 3 responsabilities:
        - knows who needs to call to validate data
        - knows what services needs to call to make the desired operation
        - knows who needs to call to build the response and returns it
        """
        # --------------------- validates and get data --------------------- #
        book: BookModel = get_object_or_404(BookModel, uid=uid)
        # clean way to validate if Book exists and if it doesn't the function
        # will respond with a http 404 response.

        # ---------------- build the response and return it ---------------- #
        return Response(data=BookSerializer(book).data)