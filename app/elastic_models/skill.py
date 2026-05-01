from elasticsearch_dsl import Document, Integer, Text, Keyword, connections


class SkillDoc(Document):
    form_id = Integer()

    name = Text(
        analyzer='english',
        fields={'raw': Keyword()}
    )

    description = Text(analyzer='english')
    type = Keyword()

    class Index:
        name = 'skills'  # Имя индекса в ES
