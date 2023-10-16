from sparknlp.annotator import SuperBertSentenceEmbeddings


class SuperBertSentence:
    @staticmethod
    def get_default_model():
        return SuperBertSentenceEmbeddings.pretrained() \
        .setInputCols("sentence") \
        .setOutputCol("sentence_embeddings")

    @staticmethod
    def get_pretrained_model(name, language, bucket=None):
        return SuperBertSentenceEmbeddings.pretrained(name,language,bucket) \
            .setInputCols('sentence') \
            .setOutputCol("sentence_embeddings")



