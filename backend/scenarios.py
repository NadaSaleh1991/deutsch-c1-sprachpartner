"""C1-level roleplay scenarios for the German immersion tutor.

Each scenario drops the learner into a realistic, register-appropriate
situation (bureaucracy, negotiation, medical, academic, ...) that a C1
speaker is expected to be able to handle: forming arguments, hedging,
being persuasive/assertive, and reacting to pushback.
"""

SCENARIOS = [
    {
        "id": "mietminderung",
        "title": "Mietminderung wegen Schimmel",
        "emoji": "🏚️",
        "setting": "Telefonat mit der Hausverwaltung",
        "ai_persona": (
            "Herr Brandt, Mitarbeiter der Hausverwaltung Rheinblick GmbH. "
            "Sachlich, leicht genervt, verweist gern auf Verträge, Fristen und "
            "Zuständigkeiten und gibt nicht sofort nach."
        ),
        "learner_role": (
            "Mieter/in, der/die seit drei Wochen Schimmel im Schlafzimmer meldet, "
            "ohne dass etwas passiert ist."
        ),
        "goal": (
            "Eine Mietminderung von etwa 20% durchsetzen und eine verbindliche "
            "Frist zur Mängelbeseitigung vereinbaren."
        ),
        "register": "formell, sachlich-bestimmt",
        "opening_line": (
            "Hausverwaltung Rheinblick, Brandt, guten Tag. Sie rufen sicher wegen "
            "Ihrer E-Mail an – aber ich sage gleich: Für Mietminderungen sind wir "
            "nicht zuständig, das regelt der Vermieter direkt."
        ),
        "key_phrases": [
            "Ich sehe mich gezwungen, ...",
            "Laut § 536 BGB steht mir ... zu",
            "Ich setze Ihnen hiermit eine Frist bis zum ...",
            "Sollte sich bis dahin nichts ändern, behalte ich mir vor, ...",
        ],
    },
    {
        "id": "gehaltsverhandlung",
        "title": "Gehaltsverhandlung",
        "emoji": "💼",
        "setting": "Mitarbeitergespräch im Büro",
        "ai_persona": (
            "Frau Dr. Wessel, Abteilungsleiterin. Wohlwollend, aber budgetbewusst; "
            "verhandelt hart, bleibt aber fair und sachlich."
        ),
        "learner_role": "Mitarbeiter/in mit zwei Jahren Betriebszugehörigkeit.",
        "goal": (
            "Eine Gehaltserhöhung von mindestens 8% erreichen, gestützt auf "
            "konkrete eigene Erfolge."
        ),
        "register": "formell, professionell, überzeugend",
        "opening_line": (
            "Schön, dass Sie sich Zeit nehmen. Ich habe gesehen, Sie wollten über "
            "Ihr Gehalt sprechen – erzählen Sie mir, was Sie sich vorstellen."
        ),
        "key_phrases": [
            "Vor dem Hintergrund, dass ...",
            "Ich würde mir wünschen, dass ...",
            "Wie stehen Sie dazu, wenn wir ...",
            "Um auf einen gemeinsamen Nenner zu kommen, ...",
        ],
    },
    {
        "id": "widerspruch_bescheid",
        "title": "Widerspruch beim Bürgeramt",
        "emoji": "🏛️",
        "setting": "Am Schalter im Bürgeramt",
        "ai_persona": (
            "Frau Kaya, Sachbearbeiterin. Korrekt, an Vorschriften gebunden, aber "
            "grundsätzlich gesprächsbereit, wenn man sachlich argumentiert."
        ),
        "learner_role": "Antragsteller/in, dessen Elterngeld-Antrag abgelehnt wurde.",
        "goal": (
            "Formell Widerspruch gegen den Bescheid einlegen und die nächsten "
            "Schritte im Verfahren klären."
        ),
        "register": "formell, amtssprachlich-nüchtern",
        "opening_line": (
            "Guten Tag, Sie kommen bestimmt wegen des Bescheids. Was genau ist "
            "Ihr Anliegen?"
        ),
        "key_phrases": [
            "Hiermit lege ich Widerspruch ein gegen ...",
            "Nach meinem Verständnis der Rechtslage ...",
            "Könnten Sie mir bitte erläutern, weshalb ...",
            "Ich bitte um eine schriftliche Begründung.",
        ],
    },
    {
        "id": "zweitmeinung_arzt",
        "title": "Zweitmeinung beim Facharzt",
        "emoji": "🩺",
        "setting": "Sprechzimmer eines Orthopäden",
        "ai_persona": (
            "Dr. Novak, Orthopäde. Fachlich versiert, nimmt sich Zeit, nutzt aber "
            "gerne Fachbegriffe, die man hinterfragen muss."
        ),
        "learner_role": "Patient/in, dem eine Operation am Knie empfohlen wurde.",
        "goal": (
            "Die empfohlene Operation kritisch hinterfragen und konkrete "
            "Alternativen sowie Risiken erfragen."
        ),
        "register": "formell, aber persönlich betroffen",
        "opening_line": (
            "Guten Tag, setzen Sie sich. Ihr Hausarzt hat mir die Bilder bereits "
            "geschickt – ich würde tatsächlich zu einer Operation raten."
        ),
        "key_phrases": [
            "Was spricht aus Ihrer Sicht gegen eine konservative Behandlung?",
            "Mir wurde bereits mitgeteilt, dass ...",
            "Wie hoch schätzen Sie das Risiko von ... ein?",
            "Gibt es alternative Behandlungsmethoden?",
        ],
    },
    {
        "id": "seminar_digitalisierung",
        "title": "Seminardiskussion: Digitalisierung & Arbeitswelt",
        "emoji": "🎓",
        "setting": "Universitätsseminar",
        "ai_persona": (
            "Prof. Dr. Lindqvist, Dozent/in. Fordert klare Argumente, hakt "
            "kritisch nach und moderiert die Diskussion streng."
        ),
        "learner_role": "Studierende/r, der/die eine These vertreten soll.",
        "goal": (
            "Eine eigene These zur Digitalisierung der Arbeitswelt vertreten und "
            "überzeugend auf Gegenargumente eingehen."
        ),
        "register": "formell, akademisch, argumentativ",
        "opening_line": (
            "Gut, dann eröffnen Sie doch die Diskussion: Führt die Digitalisierung "
            "zu mehr oder zu weniger Arbeitsplatzsicherheit?"
        ),
        "key_phrases": [
            "Dem würde ich insofern widersprechen, als ...",
            "Man muss differenzieren zwischen ...",
            "Zugespitzt formuliert bedeutet das ...",
            "Empirisch lässt sich zeigen, dass ...",
        ],
    },
    {
        "id": "kundenservice_beschwerde",
        "title": "Beschwerde beim Kundenservice",
        "emoji": "📦",
        "setting": "Telefonhotline eines Elektronikversands",
        "ai_persona": (
            "Herr Ostrowski, Kundenservice-Mitarbeiter. Freundlich, folgt "
            "Skripten, gibt Kulanz nur ungern und erst nach Nachdruck."
        ),
        "learner_role": (
            "Kunde/Kundin mit einem defekten Gerät, dessen Garantie vor kurzem "
            "abgelaufen ist."
        ),
        "goal": (
            "Eine kostenlose Reparatur oder Rückerstattung außerhalb der "
            "Standard-Kulanzfrist erwirken."
        ),
        "register": "formell bis leicht ungehalten, aber höflich",
        "opening_line": (
            "Kundenservice, mein Name ist Ostrowski, was kann ich für Sie tun?"
        ),
        "key_phrases": [
            "Ich kann nicht nachvollziehen, weshalb ...",
            "Als Kunde erwarte ich, dass ...",
            "Gibt es keine Möglichkeit, kulanterweise ...",
            "Andernfalls sehe ich mich gezwungen, ...",
        ],
    },
    {
        "id": "wohnungsuebergabe",
        "title": "Wohnungsübergabe aushandeln",
        "emoji": "🔑",
        "setting": "In der leeren Wohnung bei der Schlüsselübergabe",
        "ai_persona": (
            "Frau Ecker, Vermieterin. Misstrauisch, listet akribisch vermeintliche "
            "Mängel auf und will Abzüge von der Kaution durchsetzen."
        ),
        "learner_role": "Ausziehende/r Mieter/in.",
        "goal": (
            "Unberechtigte Abzüge von der Kaution abwenden und ein faires "
            "Übergabeprotokoll erzielen."
        ),
        "register": "formell, konfliktfähig, sachlich bestimmt",
        "opening_line": (
            "So, dann schauen wir uns das mal an. Ich sage gleich: Da sind einige "
            "Dinge, die mir gar nicht gefallen."
        ),
        "key_phrases": [
            "Diese Abnutzung fällt unter normale Gebrauchsspuren.",
            "Ich bestehe darauf, dass wir das schriftlich festhalten.",
            "Dem kann ich so nicht zustimmen, weil ...",
            "Laut Übergabeprotokoll beim Einzug war das bereits ...",
        ],
    },
    {
        "id": "fuehrungsposition_interview",
        "title": "Vorstellungsgespräch: Führungsposition",
        "emoji": "🧑‍💼",
        "setting": "Video-Vorstellungsgespräch",
        "ai_persona": (
            "Herr Dr. Abasi, Personalleiter. Anspruchsvoll, stellt hypothetische "
            "Führungs- und Konfliktszenarien und hakt bei vagen Antworten nach."
        ),
        "learner_role": "Bewerber/in für eine Teamleitungsposition.",
        "goal": (
            "Führungskompetenz und Konfliktfähigkeit anhand konkreter eigener "
            "Beispiele überzeugend darstellen."
        ),
        "register": "formell, professionell, reflektiert",
        "opening_line": (
            "Schön, dass es klappt. Erzählen Sie mir doch: Wie gehen Sie mit "
            "einem Teammitglied um, das Ihre Entscheidungen offen infrage stellt?"
        ),
        "key_phrases": [
            "In einer vergleichbaren Situation habe ich ...",
            "Mein Führungsstil zeichnet sich dadurch aus, dass ...",
            "Rückblickend würde ich sagen, dass ...",
            "Mir ist wichtig, dass ...",
        ],
    },
]


def get_scenario(scenario_id: str) -> dict:
    for scenario in SCENARIOS:
        if scenario["id"] == scenario_id:
            return scenario
    raise ValueError(f"Unknown scenario id: {scenario_id}")
