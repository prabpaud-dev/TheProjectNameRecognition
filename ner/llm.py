from ner.utils import load_jsonl, save_responses_to_jsonl

# entities the LLM chat gave for the first 10 documents (id -> label -> strings)
LLM_ENTITIES = {
    "test-0001": {
        "PERSON_NAME": ["Patricia Giménez Domínguez", "Tomás Romero Domínguez", "Inés Suárez Giménez"],
        "ID_CARD_NUMBER": ["12082063W", "12082200R"],
        "ADDRESS": ["Avenida de Aragón, 102, 2-B, 17001 Girona", "Calle de la Estación, 38, 6-2a, 08221 Terrassa"],
        "REGISTRATION_NUMBER": ["ASS-2018-43226", "ENT-2018-43263", "RES-2018-43300"],
        "DATE": ["2018-04-09", "15 de abril de 2018", "21/04/2018", "2018-04-27", "3 de mayo de 2018",
                 "09/05/2018", "2018-05-15", "21 de mayo de 2018"],
        "AMOUNT": ["4.416,13 euros", "1.107,16 EUR", "5.523,29 €", "932,80 euros"],
        "ORGANIZATION": ["Servicio de Procedimientos Públicos de la Región Central",
                         "Instituto de Coordinación Territorial del Área Metropolitana",
                         "Unidad de Atención Ciudadana de la Comarca Interior",
                         "Dirección de Supervisión Administrativa de Servicios Intermunicipales"],
    },
    "test-0002": {
        "PERSON_NAME": ["David Iglesias Hernández", "Roser Prieto Serrano", "Pau Cabrera Ruiz"],
        "ID_CARD_NUMBER": ["12070281L", "12070418H"],
        "ADDRESS": ["Carrer de la Creu, 206, 6-A, 08911 Badalona", "Passeig del Comerç, 115, 6-1a, 08911 Badalona"],
        "REGISTRATION_NUMBER": ["EXP-2018-38453", "ENT-2018-38490", "RES-2018-38527"],
        "DATE": ["2018-02-20", "26 de febrer de 2018", "04/03/2018", "2018-03-10", "16 de març de 2018",
                 "22/03/2018", "2018-03-28", "3 de abril de 2018"],
        "AMOUNT": ["1.581,26 euros", "782,05 EUR", "2.363,31 €", "331,37 euros"],
        "ORGANIZATION": ["Centre de Coordinació Territorial de l'Àrea Metropolitana",
                         "Agència de Verificació Documental de les Comarques Gironines",
                         "Oficina de Gestió Administrativa de la Catalunya Central",
                         "Servei d'Atenció Ciutadana del Gironès"],
    },
    "test-0003": {
        "PERSON_NAME": ["Laura Torres Hernández", "Inés Iglesias Gómez", "Álvaro Ramírez Moreno"],
        "ID_CARD_NUMBER": ["12076583L", "12076720H"],
        "ADDRESS": ["Rambla de los Olmos, 163, 6-3a, 50001 Zaragoza", "Calle del Parque, 12, 5-2a, 46001 València"],
        "REGISTRATION_NUMBER": ["EXP/2026/41006", "ENT-2026-41043", "RES-2026-41080"],
        "DATE": ["2026-01-27", "8 de febrero de 2026", "14/02/2026", "2026-02-20", "26 de febrero de 2026",
                 "04/03/2026", "2026-03-10", "16 de marzo de 2026"],
        "AMOUNT": ["3.379,30 euros", "1.082,78 EUR", "4.462,08 €", "240,50 euros"],
        "ORGANIZATION": ["Oficina de Trámites y Registro de Coordinación Provincial",
                         "Centro de Servicios Públicos del Área Territorial Oeste",
                         "Servicio de Atención Ciudadana del Corredor Mediterráneo",
                         "Centro de Atención Ciudadana de la Zona Litoral"],
    },
    "test-0004": {
        "PERSON_NAME": ["Berta Moreno Ferrer", "Dídac Reyes Serrano", "Jordi Ferrer Ramírez"],
        "ID_CARD_NUMBER": ["12068637P", "12068774F"],
        "ADDRESS": ["Rambla del Segre, 9, 7-B, 43201 Reus", "Plaça de la Pau, 48, 2-2a, 46001 València"],
        "REGISTRATION_NUMBER": ["TRM-2018-37787", "ENT-2018-37824", "RES-2018-37861"],
        "DATE": ["27/05/2018", "2018-06-02", "8 de juny de 2018", "14/06/2018", "2018-06-20",
                 "26 de juny de 2018", "02/07/2018", "2018-07-08"],
        "AMOUNT": ["2.644,97 €", "521,62 euros", "3.166,59 EUR", "564,05 €"],
        "ORGANIZATION": ["Direcció de Planificació Local de Ponent", "Unitat de Planificació Local del Gironès",
                         "Servei de Serveis Públics del Segrià", "Centre de Tràmits i Registre del Gironès"],
    },
    "test-0005": {
        "PERSON_NAME": ["Carmen Roca Campos", "Hugo Ruiz Arias", "Javier López Ramírez"],
        "ID_CARD_NUMBER": ["12078775A", "12078912W"],
        "ADDRESS": ["Plaza de los Olmos, 205, 5-3a, 08500 Vic", "Avenida de los Olmos, 176, 2-B, 25001 Lleida"],
        "REGISTRATION_NUMBER": ["ASS-2021-41894", "ENT-2021-41931", "RES-2021-41968"],
        "DATE": ["2021-12-13", "19 de diciembre de 2021", "25/12/2021", "2021-12-31", "6 de enero de 2022",
                 "12/01/2022", "2022-01-24", "30 de enero de 2022"],
        "AMOUNT": ["4.991,19 euros", "255,26 EUR", "5.246,45 €", "937,53 euros"],
        "ORGANIZATION": ["Servicio de Atención Ciudadana del Distrito Sur",
                         "Dirección de Procedimientos Públicos del Distrito Sur",
                         "Consorcio de Gestión Económica de la Comarca Interior",
                         "Oficina de Servicios Públicos de la Región Central"],
    },
    "test-0006": {
        "PERSON_NAME": ["Xavier Ramos Torres", "Laia Serrano Castro", "Raquel Prieto Vila"],
        "ID_CARD_NUMBER": ["12069185G", "12069322A"],
        "ADDRESS": ["Rambla de les Corts, 136, 3-2a, 08911 Badalona", "Carrer de la Unió, 158, 4-1a, 43201 Reus"],
        "REGISTRATION_NUMBER": ["ASS-2023-38009", "ENT-2023-38046", "RES/2023/38083"],
        "DATE": ["2023-04-19", "1 de maig de 2023", "07/05/2023", "2023-05-31", "12 de juny de 2023",
                 "24/06/2023", "2023-06-30", "30 de juliol de 2023"],
        "AMOUNT": ["5.446,05 euros", "171,35 EUR", "5.617,40 €", "533,25 euros"],
        "ORGANIZATION": ["Unitat de Gestió Econòmica del Camp de Tarragona", "Servei de Gestió Econòmica del Segrià",
                         "Oficina de Gestió Econòmica del Camp de Tarragona",
                         "Consorci de Tràmits i Registre del Vallès Occidental"],
    },
    "test-0007": {
        "PERSON_NAME": ["Jordi Aguilar Sánchez", "Neus Ramírez Roca", "Arnau Navarro Campos"],
        "ID_CARD_NUMBER": ["12074665X", "12074802D"],
        "ADDRESS": ["Passeig de la Riera, 148, 5-3a, 08001 Barcelona", "Plaça del Mercat, 17, 5-C, 08500 Vic"],
        "REGISTRATION_NUMBER": ["EXP-2020-40229", "ENT/2020/40266", "RES/2020/40303"],
        "DATE": ["2020-02-10", "16 de febrer de 2020", "22/02/2020", "2020-02-28", "5 de març de 2020",
                 "11/03/2020", "2020-03-17", "23 de març de 2020"],
        "AMOUNT": ["3.814,06 euros", "401,29 EUR", "4.215,35 €", "555,89 euros"],
        "ORGANIZATION": ["Servei de Supervisió Administrativa de les Comarques Gironines",
                         "Consorci de Serveis Públics del Camp de Tarragona",
                         "Unitat de Serveis Urbans del Segrià", "Unitat de Gestió Administrativa del Tarragonès"],
    },
    "test-0008": {
        "PERSON_NAME": ["David Campos Molina", "Teresa Ferrer Gil", "Pau Torres Gil"],
        "ID_CARD_NUMBER": ["12071925F", "12072062Y"],
        "ADDRESS": ["Passeig del Segre, 173, 8-2a, 28001 Madrid", "Avinguda del Montseny, 67, 2-B, 28001 Madrid"],
        "REGISTRATION_NUMBER": ["TRM-2021-39119", "ENT-2021-39156", "RES-2021-39193"],
        "DATE": ["26/10/2021", "2021-11-01", "7 de novembre de 2021", "13/11/2021", "2021-11-19",
                 "25 de novembre de 2021", "01/12/2021", "2021-12-07"],
        "AMOUNT": ["2.956,20 €", "602,20 euros", "3.558,40 EUR", "528,14 €"],
        "ORGANIZATION": ["Centre de Verificació Documental del Segrià", "Oficina d'Atenció Ciutadana del Maresme",
                         "Unitat de Recursos Municipals del Segrià",
                         "Institut de Serveis Urbans del Vallès Oriental"],
    },
    "test-0009": {
        "PERSON_NAME": ["David Molina Rubio", "Raquel Navarro Guerrero", "David Suárez Suárez"],
        "ID_CARD_NUMBER": ["12075213Y", "12075350M"],
        "ADDRESS": ["Plaça de la Unió, 207, 5-2a, 03001 Alacant", "Avinguda de la Riera, 15, 3-3a, 08301 Mataró"],
        "REGISTRATION_NUMBER": ["EXP-2026-40451", "ENT/2026/40488", "RES/2026/40525"],
        "DATE": ["2026-05-09", "15 de maig de 2026", "21/05/2026", "2026-05-27", "2 de juny de 2026",
                 "08/06/2026", "2026-06-14", "20 de juny de 2026"],
        "AMOUNT": ["3.219,11 euros", "906,83 EUR", "4.125,94 €", "442,69 euros"],
        "ORGANIZATION": ["Direcció de Verificació Documental del Maresme",
                         "Servei de Planificació Local del Vallès Oriental",
                         "Institut de Tràmits i Registre de la Catalunya Central",
                         "Servei de Verificació Documental de les Comarques Gironines"],
    },
    "test-0010": {
        "PERSON_NAME": ["Adriana Aguilar Serrano", "Emilio Alonso Ferrer", "Patricia Aguilar Roca"],
        "ID_CARD_NUMBER": ["12081515Y", "12081652M"],
        "ADDRESS": ["Rambla de la Fuente, 1, 7-A, 08500 Vic", "Paseo de la Sierra, 25, 5-1a, 43001 Tarragona"],
        "REGISTRATION_NUMBER": ["EXP-2023-43004", "ENT/2023/43041", "RES-2023-43078"],
        "DATE": ["2023-11-09", "15 de noviembre de 2023", "09/12/2023", "2023-12-27", "8 de enero de 2024",
                 "14/01/2024", "2024-01-20", "26 de enero de 2024"],
        "AMOUNT": ["4.677,70 euros", "378,69 EUR", "5.056,39 €", "206,64 euros"],
        "ORGANIZATION": ["Consorcio de Trámites y Registro del Área Territorial Oeste",
                         "Servicio de Supervisión Administrativa de la Comarca Interior",
                         "Centro de Gestión Administrativa de Servicios Intermunicipales",
                         "Oficina de Supervisión Administrativa del Corredor Mediterráneo"],
    },
}


def locate_entities(text, labelled):
    # find every occurrence of each string, longest first, skipping overlaps
    items = sorted(
        ((s, label) for label, strings in labelled.items() for s in strings),
        key=lambda item: -len(item[0]),
    )
    taken: list[tuple[int, int]] = []
    found: list[dict] = []
    for string, label in items:
        start = text.find(string)
        if start == -1:
            raise ValueError(f"String not found in document: {string!r}")
        while start != -1:
            end = start + len(string)
            if all(end <= s or start >= e for s, e in taken):
                taken.append((start, end))
                found.append({"start": start, "end": end, "label": label, "text": string})
            start = text.find(string, end)
    return sorted(found, key=lambda e: e["start"])


def build_llm_predictions(validation_path, output_path):
    gold = {record["id"]: record for record in load_jsonl(validation_path)}
    responses = []
    for document_id, labelled in LLM_ENTITIES.items():  # dict order = file order (test-0001..)
        text = gold[document_id]["text"]
        responses.append({"id": document_id, "text": text, "entities": locate_entities(text, labelled)})
    save_responses_to_jsonl(responses, output_path)
    return responses
