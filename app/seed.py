from app.models import Course, Module, Lesson


def seed_data():
    from app import db

    if Course.query.first():
        return  # Already seeded

    courses_data = [
        {
            'name': 'Educação Ambiental',
            'description': 'Estudo sobre sustentabilidade, ecossistemas e impacto ambiental nas comunidades modernas.',
            'modules': [
                {
                    'name': 'Módulo 1 – Fundamentos',
                    'order': 1,
                    'lessons': [
                        {'title': 'Aula 1 – Introdução à Ecologia', 'content': 'Aqui contamos sobre os fundamentos da ecologia e seus conceitos básicos.', 'order': 1},
                        {'title': 'Atividade 1 – Mapa Conceitual', 'content': 'Crie um mapa conceitual sobre os biomas brasileiros.', 'order': 2},
                    ]
                },
                {
                    'name': 'Módulo 2 – Impacto Humano',
                    'order': 2,
                    'lessons': [
                        {'title': 'Aula 2 – Desmatamento', 'content': 'Análise das causas e consequências do desmatamento global.', 'order': 1},
                        {'title': 'PDF da Aula', 'content': 'Material de apoio em PDF.', 'pdf_url': '#', 'order': 2},
                    ]
                },
                {
                    'name': 'Módulo 3 – Soluções',
                    'order': 3,
                    'lessons': [
                        {'title': 'Aula 3 – Energias Renováveis', 'content': 'Como as energias renováveis podem mitigar o aquecimento global.', 'order': 1},
                    ]
                },
                {
                    'name': 'Módulo 4 – Avaliação',
                    'order': 4,
                    'lessons': [
                        {'title': 'Projeto Final', 'content': 'Elabore um plano de ação sustentável para sua comunidade.', 'order': 1},
                    ]
                },
            ]
        },
        {
            'name': 'Informática',
            'description': 'Introdução à computação, redes, sistemas operacionais e programação básica.',
            'modules': [
                {
                    'name': 'Módulo 1 – Hardware',
                    'order': 1,
                    'lessons': [
                        {'title': 'Aula 1 – Componentes do Computador', 'content': 'Aqui contamos sobre os componentes físicos de um computador moderno.', 'order': 1},
                        {'title': 'Atividade 1 – Identificação de Peças', 'content': 'Identifique e descreva os componentes de um computador.', 'order': 2},
                    ]
                },
                {
                    'name': 'Módulo 2 – Software',
                    'order': 2,
                    'lessons': [
                        {'title': 'Aula 2 – Sistemas Operacionais', 'content': 'Estudo comparativo entre Windows, Linux e macOS.', 'order': 1},
                        {'title': 'PDF da Aula', 'content': 'Material de apoio em PDF.', 'pdf_url': '#', 'order': 2},
                    ]
                },
                {
                    'name': 'Módulo 3 – Redes',
                    'order': 3,
                    'lessons': [
                        {'title': 'Aula 3 – Fundamentos de Redes', 'content': 'Protocolos, topologias e arquitetura cliente-servidor.', 'order': 1},
                    ]
                },
                {
                    'name': 'Módulo 4 – Programação',
                    'order': 4,
                    'lessons': [
                        {'title': 'Aula 4 – Lógica de Programação', 'content': 'Variáveis, condicionais, loops e funções.', 'order': 1},
                    ]
                },
            ]
        },
    ]

    for course_data in courses_data:
        course = Course(
            name=course_data['name'],
            description=course_data['description']
        )
        db.session.add(course)
        db.session.flush()

        for mod_data in course_data['modules']:
            module = Module(
                name=mod_data['name'],
                order=mod_data['order'],
                course_id=course.id
            )
            db.session.add(module)
            db.session.flush()

            for lesson_data in mod_data['lessons']:
                lesson = Lesson(
                    title=lesson_data['title'],
                    content=lesson_data['content'],
                    pdf_url=lesson_data.get('pdf_url'),
                    order=lesson_data['order'],
                    module_id=module.id
                )
                db.session.add(lesson)

    db.session.commit()
    print("✅ Seed data inserted.")
