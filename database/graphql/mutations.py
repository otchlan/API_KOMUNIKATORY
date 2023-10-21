import graphene
from database.models.message_model import Message
from .types import MessageType  # Będziesz musiał stworzyć ten typ

class CreateMessage(graphene.Mutation):
    class Arguments:
        subject = graphene.String(required=True)
        sender = graphene.String(required=True)
        content = graphene.String(required=True)
    
    ok = graphene.Boolean()
    message = graphene.Field(lambda: MessageType)
    
    def mutate(root, info, subject, sender, content):
        message = Message(subject=subject, sender=sender, content=content)
        # Dodaj logikę zapisu do bazy danych
        return CreateMessage(message=message, ok=True)

class Mutation(graphene.ObjectType):
    create_message = CreateMessage.Field()
