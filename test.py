def doc_gen(num=1):
    """Generator, yielding test mongo output"""
    for i in range(num):
        yield (i, { "subject": "song",
                    "content": "The pope had a dog",
                    "published": "1012325463"   })

