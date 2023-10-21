import graphene
from database.models.message_model import Message
from .types import MessageType  # Będziesz musiał stworzyć ten typ

class Query(graphene.ObjectType):
    message = graphene.Field(MessageType, id=graphene.Int(required=True))
    
    def resolve_message(root, info, id):
        # Znajdź i zwróć wiadomość na podstawie ID
        pass
