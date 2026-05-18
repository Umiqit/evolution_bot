#!/usr/bin/env python3
# create_final_bank.py

import json
import os

def create_final_bank():
    """Создает банк из 10 сценариев по 4 этапа с реальными видами"""
    
    bank = {
        "scenarios": [
            {
                "id": "forest_tits",
                "title": "🌳 Большие синицы",
                "description": "Эволюция синиц в смешанном лесу",
                "stages": [
                    {
                        "description": "Популяция больших синиц (300 особей) обитает в лесу. Основной корм - гусеницы. Зимы холодные, конкуренция с другими птицами высокая.",
                        "choices": [
                            {
                                "text": "Увеличить клюв",
                                "is_correct": False,
                                "effect": {"beak_size": 30, "viability_index": -10, "energy_reserve": -20}
                            },
                            {
                                "text": "Расширить рацион",
                                "is_correct": True,
                                "effect": {"diet_diversity": 40, "viability_index": 20, "energy_reserve": 15}
                            },
                            {
                                "text": "Усилить конкуренцию",
                                "is_correct": False,
                                "effect": {"aggression": 50, "viability_index": -25}
                            }
                        ],
                        "scientific_explanation": "Большие синицы известны своей способностью расширять рацион в неблагоприятных условиях, переключаясь на семена и корма у кормушек.",
                        "environment_changes": {"temperature": -5, "food": -20},
                        "feedback_correct": "Синицы начали использовать разные корма, выживаемость повысилась.",
                        "feedback_incorrect": "Узкая специализация привела к голоду зимой."
                    },
                    {
                        "description": "Появился конкурент - лазоревки, которые лучше собирают гусениц с веток.",
                        "choices": [
                            {
                                "text": "Кормиться у кормушек",
                                "is_correct": True,
                                "effect": {"synanthropy": 60, "viability_index": 30, "energy_reserve": 40}
                            },
                            {
                                "text": "Искать другой корм",
                                "is_correct": True,
                                "effect": {"diet_diversity": 50, "viability_index": 20}
                            },
                            {
                                "text": "Конкурировать с ними",
                                "is_correct": False,
                                "effect": {"aggression": 60, "viability_index": -40}
                            }
                        ],
                        "scientific_explanation": "Синицы часто выигрывают конкуренцию за счет синантропизации - использования кормушек и близости к человеку.",
                        "environment_changes": {"competition": 30},
                        "feedback_correct": "Синицы освоили кормушки и успешно переживают зиму.",
                        "feedback_incorrect": "Прямая конкуренция истощила популяцию."
                    },
                    {
                        "description": "Зима аномально холодная. Многие птицы погибли.",
                        "choices": [
                            {
                                "text": "Усилить терморегуляцию",
                                "is_correct": True,
                                "effect": {"cold_resistance": 50, "viability_index": 30, "energy_reserve": -20}
                            },
                            {
                                "text": "Ночлеги в дуплах",
                                "is_correct": True,
                                "effect": {"roosting": 70, "viability_index": 25}
                            },
                            {
                                "text": "Мигрировать на юг",
                                "is_correct": False,
                                "effect": {"migration": 100, "viability_index": -50, "energy_reserve": -80}
                            }
                        ],
                        "scientific_explanation": "Синицы - оседлые птицы, они адаптируются к холоду за счет усиленного метаболизма и ночевок в укрытиях.",
                        "environment_changes": {"temperature": -15},
                        "feedback_correct": "Синицы пережили холода благодаря адаптациям.",
                        "feedback_incorrect": "Миграция в никуда привела к гибели."
                    },
                    {
                        "description": "Весна. Выжило 120 синиц, адаптированных к жизни рядом с человеком.",
                        "choices": [
                            {
                                "text": "Закрепить признак",
                                "is_correct": True,
                                "effect": {"urban": 80, "viability_index": 40, "rare_species": "city_tit"}
                            },
                            {
                                "text": "Вернуться в лес",
                                "is_correct": False,
                                "effect": {"forest": 50, "viability_index": -20}
                            },
                            {
                                "text": "Сохранить гибкость",
                                "is_correct": True,
                                "effect": {"adaptability": 70, "viability_index": 30}
                            }
                        ],
                        "scientific_explanation": "Синицы успешно адаптировались к урбанизированной среде, став обычными городскими птицами.",
                        "environment_changes": {"urban": 50},
                        "feedback_correct": "Сформировалась городская популяция синиц.",
                        "feedback_incorrect": "В лесу слишком много конкурентов."
                    }
                ],
                "initial_population": {
                    "genome_attributes": {
                        "colors": {"yellow": 200, "green": 150, "blue": 100},
                        "beak_size": 50,
                        "diet_diversity": 30,
                        "cold_resistance": 40,
                        "synanthropy": 10
                    },
                    "viability_index": 100,
                    "energy_reserve": 100,
                    "current_environment": {"type": "forest", "season": "autumn", "temperature": 10, "food": 80}
                },
                "rare_species": ["city_tit"]
            },
            {
                "id": "desert_geckos",
                "title": "🦎 Пустынные гекконы",
                "description": "Адаптация гекконов к условиям пустыни",
                "stages": [
                    {
                        "description": "Популяция гекконов (200 особей) в песчаной пустыне. Днем +45°C, ночью +15°C. Воды нет.",
                        "choices": [
                            {
                                "text": "Стать ночными",
                                "is_correct": True,
                                "effect": {"nocturnal": 80, "night_vision": 50, "viability_index": 30}
                            },
                            {
                                "text": "Развить терморегуляцию",
                                "is_correct": False,
                                "effect": {"heat_tolerance": 60, "viability_index": -20}
                            },
                            {
                                "text": "Рыть глубокие норы",
                                "is_correct": True,
                                "effect": {"burrowing": 70, "viability_index": 25}
                            }
                        ],
                        "scientific_explanation": "Пустынные гекконы ведут ночной образ жизни, избегая дневной жары, и прячутся в норах.",
                        "environment_changes": {"temperature": 45},
                        "feedback_correct": "Гекконы стали активны ночью, днем прячутся в норах.",
                        "feedback_incorrect": "Дневная активность привела к перегреву и гибели."
                    },
                    {
                        "description": "В пустыне появились змеи, охотящиеся в норах.",
                        "choices": [
                            {
                                "text": "Убегать по песку",
                                "is_correct": True,
                                "effect": {"speed": 60, "sand_running": 70, "viability_index": 25}
                            },
                            {
                                "text": "Лазать по камням",
                                "is_correct": False,
                                "effect": {"climbing": 70, "viability_index": -30}
                            },
                            {
                                "text": "Маскировка под песок",
                                "is_correct": True,
                                "effect": {"camouflage": 80, "viability_index": 35}
                            }
                        ],
                        "scientific_explanation": "Гекконы рода Stenodactylus развили способность быстро бегать по сыпучему песку, спасаясь от змей.",
                        "environment_changes": {"predators": 40},
                        "feedback_correct": "Гекконы научились быстро убегать и маскироваться.",
                        "feedback_incorrect": "Камней в пустыне мало, лазанье не помогло."
                    },
                    {
                        "description": "Змеи стали быстрее. Нужно новое решение.",
                        "choices": [
                            {
                                "text": "Автотомия хвоста",
                                "is_correct": True,
                                "effect": {"tail_autotomy": 90, "viability_index": 30, "energy_reserve": -20}
                            },
                            {
                                "text": "Ядовитая слюна",
                                "is_correct": False,
                                "effect": {"venom": 50, "viability_index": -40}
                            },
                            {
                                "text": "Жить группами",
                                "is_correct": False,
                                "effect": {"social": 60, "viability_index": -10}
                            }
                        ],
                        "scientific_explanation": "Многие гекконы отбрасывают хвост, отвлекая хищника, а затем регенерируют его.",
                        "environment_changes": {"predator_speed": 30},
                        "feedback_correct": "Гекконы выживают, отбрасывая хвост.",
                        "feedback_incorrect": "Яд не развился, гекконы гибнут."
                    },
                    {
                        "description": "Популяция сократилась до 80 особей, но выжившие хорошо адаптированы.",
                        "choices": [
                            {
                                "text": "Закрепить признаки",
                                "is_correct": True,
                                "effect": {"stability": 70, "viability_index": 40, "rare_species": "sand_gecko"}
                            },
                            {
                                "text": "Освоить новые корма",
                                "is_correct": True,
                                "effect": {"diet": 60, "viability_index": 30}
                            },
                            {
                                "text": "Рискованные мутации",
                                "is_correct": False,
                                "effect": {"mutations": 100, "viability_index": -50}
                            }
                        ],
                        "scientific_explanation": "Сформировался вид пустынных гекконов с комплексом адаптаций: ночной образ жизни, быстрый бег, автотомия хвоста.",
                        "environment_changes": {},
                        "feedback_correct": "Новый вид пустынных гекконов сформирован!",
                        "feedback_incorrect": "Мутации дестабилизировали популяцию."
                    }
                ],
                "initial_population": {
                    "genome_attributes": {
                        "colors": {"sand": 150, "spotted": 50},
                        "speed": 40,
                        "nocturnal": 20,
                        "burrowing": 30,
                        "camouflage": 40,
                        "tail_autotomy": 0
                    },
                    "viability_index": 100,
                    "energy_reserve": 100,
                    "current_environment": {"type": "desert", "temperature": 45, "predators": 20}
                },
                "rare_species": ["sand_gecko"]
            },
            {
                "id": "cave_fish",
                "title": "🐟 Слепые пещерные рыбы",
                "description": "Эволюция рыб в подземных пещерах",
                "stages": [
                    {
                        "description": "Рыбы (500 особей) попали в пещеру. Полная темнота, мало еды.",
                        "choices": [
                            {
                                "text": "Атрофировать глаза",
                                "is_correct": True,
                                "effect": {"eye_size": -80, "energy_reserve": 50, "viability_index": 30}
                            },
                            {
                                "text": "Усилить зрение",
                                "is_correct": False,
                                "effect": {"eye_size": 50, "viability_index": -60}
                            },
                            {
                                "text": "Развить боковую линию",
                                "is_correct": True,
                                "effect": {"lateral_line": 80, "viability_index": 35}
                            }
                        ],
                        "scientific_explanation": "Пещерные рыбы (Astyanax mexicanus) теряют глаза, экономя энергию, и развивают органы чувств для ориентации в темноте.",
                        "environment_changes": {"light": 0, "food": -50},
                        "feedback_correct": "Глаза атрофировались, экономия энергии помогла выжить.",
                        "feedback_incorrect": "Зрение в темноте бесполезно, рыбы погибли."
                    },
                    {
                        "description": "Еды становится еще меньше. Нужны новые источники.",
                        "choices": [
                            {
                                "text": "Чувствовать химию воды",
                                "is_correct": True,
                                "effect": {"chemoreception": 80, "viability_index": 40, "energy_reserve": 20}
                            },
                            {
                                "text": "Есть все подряд",
                                "is_correct": False,
                                "effect": {"diet": 80, "viability_index": -30}
                            },
                            {
                                "text": "Замедлить метаболизм",
                                "is_correct": True,
                                "effect": {"metabolism": -40, "viability_index": 25, "energy_reserve": 60}
                            }
                        ],
                        "scientific_explanation": "Пещерные рыбы развивают хеморецепцию для поиска пищи и замедляют метаболизм в условиях дефицита ресурсов.",
                        "environment_changes": {"food": -70},
                        "feedback_correct": "Рыбы находят пищу по химическим сигналам.",
                        "feedback_incorrect": "Всеядность не помогла - рыбы отравились."
                    },
                    {
                        "description": "В пещере сильное течение. Рыб сносит потоком.",
                        "choices": [
                            {
                                "text": "Уменьшить плав.пузырь",
                                "is_correct": True,
                                "effect": {"swim_bladder": -50, "viability_index": 30}
                            },
                            {
                                "text": "Увеличить плавники",
                                "is_correct": False,
                                "effect": {"fins": 60, "viability_index": -20}
                            },
                            {
                                "text": "Жить у дна",
                                "is_correct": True,
                                "effect": {"benthic": 80, "viability_index": 35}
                            }
                        ],
                        "scientific_explanation": "Пещерные рыбы часто редуцируют плавательный пузырь, становясь придонными, чтобы не сноситься течением.",
                        "environment_changes": {"current": 50},
                        "feedback_correct": "Рыбы опустились на дно и перестали сноситься течением.",
                        "feedback_incorrect": "Большие плавники не помогли."
                    },
                    {
                        "description": "Популяция (120 особей) стабилизировалась. Рыбы полностью адаптированы к пещере.",
                        "choices": [
                            {
                                "text": "Закрепить признаки",
                                "is_correct": True,
                                "effect": {"stability": 80, "viability_index": 40, "rare_species": "cave_astyanax"}
                            },
                            {
                                "text": "Вернуться на свет",
                                "is_correct": False,
                                "effect": {"migration": 100, "viability_index": -80}
                            },
                            {
                                "text": "Сохранить изменчивость",
                                "is_correct": True,
                                "effect": {"variability": 70, "viability_index": 30}
                            }
                        ],
                        "scientific_explanation": "Слепые пещерные рыбы - классический пример эволюции в изоляции.",
                        "environment_changes": {},
                        "feedback_correct": "Сформировалась устойчивая популяция пещерных рыб.",
                        "feedback_incorrect": "Возврат на поверхность привел к гибели."
                    }
                ],
                "initial_population": {
                    "genome_attributes": {
                        "colors": {"silver": 300, "gray": 200},
                        "eye_size": 100,
                        "lateral_line": 30,
                        "chemoreception": 20,
                        "metabolism": 100,
                        "benthic": 10
                    },
                    "viability_index": 100,
                    "energy_reserve": 100,
                    "current_environment": {"type": "cave", "light": 100, "food": 50, "current": 10}
                },
                "rare_species": ["cave_astyanax"]
            },
            {
                "id": "arctic_fox",
                "title": "🦊 Песцы",
                "description": "Адаптация песцов к Арктике",
                "stages": [
                    {
                        "description": "Песцы (150 особей) в тундре. Зимой -30°C, полярная ночь.",
                        "choices": [
                            {
                                "text": "Густой мех",
                                "is_correct": True,
                                "effect": {"fur_density": 80, "viability_index": 35}
                            },
                            {
                                "text": "Жировые запасы",
                                "is_correct": True,
                                "effect": {"fat": 70, "viability_index": 30, "energy_reserve": 50}
                            },
                            {
                                "text": "Мигрировать на юг",
                                "is_correct": False,
                                "effect": {"migration": 100, "viability_index": -40}
                            }
                        ],
                        "scientific_explanation": "Песцы (Vulpes lagopus) имеют самый теплый мех среди арктических животных и накапливают жир на зиму.",
                        "environment_changes": {"temperature": -30},
                        "feedback_correct": "Густой мех и жир помогают пережить зиму.",
                        "feedback_incorrect": "Миграция истощила запасы."
                    },
                    {
                        "description": "Летом мех бурый, зимой - белый. Но снега стало меньше.",
                        "choices": [
                            {
                                "text": "Остаться бурыми",
                                "is_correct": False,
                                "effect": {"winter_color": "brown", "viability_index": -50}
                            },
                            {
                                "text": "Сезонная линька",
                                "is_correct": True,
                                "effect": {"molt": 80, "viability_index": 40}
                            },
                            {
                                "text": "Серый окрас зимой",
                                "is_correct": True,
                                "effect": {"winter_color": "gray", "viability_index": 30}
                            }
                        ],
                        "scientific_explanation": "Песцы меняют окрас по сезонам. При сокращении снежного покрова преимущество получают особи с серым зимним мехом.",
                        "environment_changes": {"snow": -40},
                        "feedback_correct": "Серый мех маскирует на фоне скал.",
                        "feedback_incorrect": "Белые песцы на бурой земле стали легкой добычей."
                    },
                    {
                        "description": "Основная добыча - лемминги. Их численность упала.",
                        "choices": [
                            {
                                "text": "Охотиться на птиц",
                                "is_correct": True,
                                "effect": {"bird_hunting": 70, "viability_index": 35}
                            },
                            {
                                "text": "За медведями",
                                "is_correct": True,
                                "effect": {"scavenging": 80, "viability_index": 30, "energy_reserve": 40}
                            },
                            {
                                "text": "Голодать",
                                "is_correct": False,
                                "effect": {"starvation": 100, "viability_index": -80}
                            }
                        ],
                        "scientific_explanation": "Песцы - оппортунисты, они следуют за белыми медведями, питаясь остатками их добычи.",
                        "environment_changes": {"lemmings": -70},
                        "feedback_correct": "Песцы переключились на альтернативные корма.",
                        "feedback_incorrect": "Специализация привела к голоду."
                    },
                    {
                        "description": "Популяция (80 особей) адаптировалась к изменениям климата.",
                        "choices": [
                            {
                                "text": "Закрепить серый окрас",
                                "is_correct": True,
                                "effect": {"gray_morph": 100, "rare_species": "gray_fox", "viability_index": 40}
                            },
                            {
                                "text": "Расширить ареал",
                                "is_correct": True,
                                "effect": {"range": 100, "viability_index": 30}
                            },
                            {
                                "text": "Вернуть белый окрас",
                                "is_correct": False,
                                "effect": {"white_morph": 100, "viability_index": -50}
                            }
                        ],
                        "scientific_explanation": "В популяциях песцов встречаются цветовые морфы. В условиях малоснежных зим серая морфа получает преимущество.",
                        "environment_changes": {"snow": -20},
                        "feedback_correct": "Серая морфа закрепилась в популяции.",
                        "feedback_incorrect": "Белые песцы не выживают."
                    }
                ],
                "initial_population": {
                    "genome_attributes": {
                        "colors": {"white": 100, "brown": 50},
                        "fur_density": 50,
                        "fat": 40,
                        "molt": 50,
                        "bird_hunting": 20,
                        "scavenging": 30
                    },
                    "viability_index": 100,
                    "energy_reserve": 100,
                    "current_environment": {"type": "tundra", "temperature": -30, "snow": 80, "lemmings": 100}
                },
                "rare_species": ["gray_fox"]
            },
            {
                "id": "island_rats",
                "title": "🐀 Островные крысы",
                "description": "Эволюция крыс на изолированном острове",
                "stages": [
                    {
                        "description": "Крысы (50 особей) попали на необитаемый остров. Хищников нет, еды много.",
                        "choices": [
                            {
                                "text": "Увеличить размер",
                                "is_correct": True,
                                "effect": {"body_size": 80, "viability_index": 30, "energy_reserve": 50}
                            },
                            {
                                "text": "Увеличить плодовитость",
                                "is_correct": False,
                                "effect": {"fecundity": 100, "viability_index": -30}
                            },
                            {
                                "text": "Освоить деревья",
                                "is_correct": True,
                                "effect": {"arboreal": 70, "viability_index": 25}
                            }
                        ],
                        "scientific_explanation": "На островах без хищников мелкие животные часто становятся крупнее (островной гигантизм) и осваивают новые ниши.",
                        "environment_changes": {"predators": 0, "food": 200},
                        "feedback_correct": "Крысы стали крупнее и освоили древесный образ жизни.",
                        "feedback_incorrect": "Перенаселение истощило ресурсы."
                    },
                    {
                        "description": "Популяция выросла до 500. Началась конкуренция за корм.",
                        "choices": [
                            {
                                "text": "Разделить ниши",
                                "is_correct": True,
                                "effect": {"niche_partition": 80, "viability_index": 40}
                            },
                            {
                                "text": "Усилить конкуренцию",
                                "is_correct": False,
                                "effect": {"competition": 100, "viability_index": -50}
                            },
                            {
                                "text": "Каннибализм",
                                "is_correct": False,
                                "effect": {"cannibalism": 70, "viability_index": -60}
                            }
                        ],
                        "scientific_explanation": "На островах виды часто разделяют ниши: одни специализируются на семенах, другие - на насекомых.",
                        "environment_changes": {"competition": 50},
                        "feedback_correct": "Крысы разделили кормовые ресурсы.",
                        "feedback_incorrect": "Жесткая конкуренция истощила популяцию."
                    },
                    {
                        "description": "На остров залетели совы. Появились хищники.",
                        "choices": [
                            {
                                "text": "Ночная активность",
                                "is_correct": True,
                                "effect": {"nocturnal": 80, "viability_index": 40}
                            },
                            {
                                "text": "Рыть норы",
                                "is_correct": True,
                                "effect": {"burrowing": 80, "viability_index": 35}
                            },
                            {
                                "text": "Драться с совами",
                                "is_correct": False,
                                "effect": {"aggression": 100, "viability_index": -80}
                            }
                        ],
                        "scientific_explanation": "При появлении хищников жертвы могут менять поведение: становиться ночными или использовать убежища.",
                        "environment_changes": {"owl_predators": 40},
                        "feedback_correct": "Крысы стали активны ночью и прячутся в норах.",
                        "feedback_incorrect": "Прямое противостояние с совами привело к гибели."
                    },
                    {
                        "description": "Популяция (300 особей) стабилизировалась. Крупные, древесные, с разделением ниш.",
                        "choices": [
                            {
                                "text": "Закрепить признаки",
                                "is_correct": True,
                                "effect": {"island_specialist": 100, "rare_species": "island_rat", "viability_index": 40}
                            },
                            {
                                "text": "Вернуться к исходному",
                                "is_correct": False,
                                "effect": {"reversion": 100, "viability_index": -50}
                            },
                            {
                                "text": "Сохранить пластичность",
                                "is_correct": True,
                                "effect": {"plasticity": 80, "viability_index": 30}
                            }
                        ],
                        "scientific_explanation": "Островные популяции часто образуют эндемичные виды с уникальными адаптациями.",
                        "environment_changes": {},
                        "feedback_correct": "Сформировался новый островной вид крыс.",
                        "feedback_incorrect": "Возврат к исходному типу невыгоден."
                    }
                ],
                "initial_population": {
                    "genome_attributes": {
                        "colors": {"gray": 30, "brown": 20},
                        "body_size": 30,
                        "arboreal": 10,
                        "nocturnal": 20,
                        "burrowing": 20
                    },
                    "viability_index": 100,
                    "energy_reserve": 100,
                    "current_environment": {"type": "island", "predators": 0, "food": 100}
                },
                "rare_species": ["island_rat"]
            },
            {
                "id": "mountain_ibex",
                "title": "🐐 Горные козлы",
                "description": "Эволюция козлов в Альпах",
                "stages": [
                    {
                        "description": "Популяция горных козлов (200 особей) на высоте 3000м. Кислорода мало, холодно, скалы.",
                        "choices": [
                            {
                                "text": "Увеличить легкие",
                                "is_correct": True,
                                "effect": {"lung_capacity": 80, "viability_index": 35, "energy_reserve": -10}
                            },
                            {
                                "text": "Густая шерсть",
                                "is_correct": True,
                                "effect": {"fur": 70, "viability_index": 30}
                            },
                            {
                                "text": "Спуститься ниже",
                                "is_correct": False,
                                "effect": {"migration": 100, "viability_index": -40}
                            }
                        ],
                        "scientific_explanation": "Горные козлы (Capra ibex) адаптированы к гипоксии за счет увеличенного объема легких и высокого содержания гемоглобина.",
                        "environment_changes": {"altitude": 3000, "temperature": -5},
                        "feedback_correct": "Козлы лучше переносят разреженный воздух.",
                        "feedback_incorrect": "Спуск вниз увеличил конкуренцию."
                    },
                    {
                        "description": "Появились волки, охотящиеся в горах.",
                        "choices": [
                            {
                                "text": "Лазать по скалам",
                                "is_correct": True,
                                "effect": {"climbing": 80, "viability_index": 40}
                            },
                            {
                                "text": "Бегать быстрее",
                                "is_correct": False,
                                "effect": {"speed": 70, "viability_index": -20}
                            },
                            {
                                "text": "Жить стадами",
                                "is_correct": True,
                                "effect": {"herd": 70, "viability_index": 30}
                            }
                        ],
                        "scientific_explanation": "Козлы спасаются от хищников, забираясь на отвесные скалы, куда волки не могут пройти.",
                        "environment_changes": {"predators": 40},
                        "feedback_correct": "Козлы уходят на скалы, волки не достают.",
                        "feedback_incorrect": "В горах от волков не убежать."
                    },
                    {
                        "description": "Зима, снег глубокий, корма мало.",
                        "choices": [
                            {
                                "text": "Копытить снег",
                                "is_correct": True,
                                "effect": {"hoof_strength": 70, "viability_index": 35}
                            },
                            {
                                "text": "Есть лишайники",
                                "is_correct": True,
                                "effect": {"diet": 60, "viability_index": 30}
                            },
                            {
                                "text": "Мигрировать в долину",
                                "is_correct": False,
                                "effect": {"migration": 100, "viability_index": -30}
                            }
                        ],
                        "scientific_explanation": "Козлы раскапывают снег копытами, добывая сухую траву, и поедают лишайники со скал.",
                        "environment_changes": {"snow": 80, "food": -50},
                        "feedback_correct": "Козлы находят корм под снегом.",
                        "feedback_incorrect": "В долине уже есть другие копытные."
                    },
                    {
                        "description": "Популяция (150 особей) хорошо адаптирована к горам.",
                        "choices": [
                            {
                                "text": "Закрепить признаки",
                                "is_correct": True,
                                "effect": {"alpine_specialist": 100, "rare_species": "alpine_ibex", "viability_index": 40}
                            },
                            {
                                "text": "Освоить новые высоты",
                                "is_correct": False,
                                "effect": {"higher": 100, "viability_index": -30}
                            },
                            {
                                "text": "Сохранить универсальность",
                                "is_correct": True,
                                "effect": {"adaptability": 70, "viability_index": 30}
                            }
                        ],
                        "scientific_explanation": "Альпийские козлы - пример успешной адаптации к экстремальным условиям высокогорий.",
                        "environment_changes": {},
                        "feedback_correct": "Сформировалась устойчивая популяция.",
                        "feedback_incorrect": "Слишком высоко - слишком сурово."
                    }
                ],
                "initial_population": {
                    "genome_attributes": {
                        "colors": {"brown": 150, "gray": 50},
                        "lung_capacity": 50,
                        "climbing": 40,
                        "herd": 50,
                        "hoof_strength": 50
                    },
                    "viability_index": 100,
                    "energy_reserve": 100,
                    "current_environment": {"type": "mountains", "altitude": 3000, "temperature": -5, "snow": 30, "predators": 20}
                },
                "rare_species": ["alpine_ibex"]
            },
            {
                "id": "jerboa",
                "title": "🐭 Пустынные тушканчики",
                "description": "Адаптация тушканчиков к пустыне",
                "stages": [
                    {
                        "description": "Тушканчики (300 особей) в пустыне. Днем жара, ночью холодно, мало еды.",
                        "choices": [
                            {
                                "text": "Длинные ноги",
                                "is_correct": True,
                                "effect": {"leg_length": 80, "speed": 60, "viability_index": 35}
                            },
                            {
                                "text": "Норы",
                                "is_correct": True,
                                "effect": {"burrowing": 80, "viability_index": 40}
                            },
                            {
                                "text": "Активность днем",
                                "is_correct": False,
                                "effect": {"diurnal": 100, "viability_index": -50}
                            }
                        ],
                        "scientific_explanation": "Тушканчики (Dipodidae) передвигаются прыжками на длинных ногах, экономя энергию, и прячутся в норах от жары.",
                        "environment_changes": {"temperature": 40},
                        "feedback_correct": "Тушканчики быстро прыгают и прячутся в норах.",
                        "feedback_incorrect": "Дневная активность привела к перегреву."
                    },
                    {
                        "description": "В пустыне появились змеи и совы.",
                        "choices": [
                            {
                                "text": "Большие уши",
                                "is_correct": True,
                                "effect": {"ears": 80, "hearing": 70, "viability_index": 35}
                            },
                            {
                                "text": "Маскировка под песок",
                                "is_correct": True,
                                "effect": {"camouflage": 70, "viability_index": 30}
                            },
                            {
                                "text": "Быть ядовитыми",
                                "is_correct": False,
                                "effect": {"venom": 50, "viability_index": -40}
                            }
                        ],
                        "scientific_explanation": "Тушканчики имеют большие уши для лучшего слуха, что помогает обнаруживать хищников на расстоянии.",
                        "environment_changes": {"predators": 50},
                        "feedback_correct": "Большие уши помогают слышать хищников.",
                        "feedback_incorrect": "Яд не развился."
                    },
                    {
                        "description": "Засуха, семян почти нет.",
                        "choices": [
                            {
                                "text": "Есть насекомых",
                                "is_correct": True,
                                "effect": {"insect_diet": 80, "viability_index": 35}
                            },
                            {
                                "text": "Не пить воду",
                                "is_correct": True,
                                "effect": {"water_from_food": 90, "viability_index": 40}
                            },
                            {
                                "text": "Впадать в спячку",
                                "is_correct": False,
                                "effect": {"hibernation": 100, "viability_index": -30}
                            }
                        ],
                        "scientific_explanation": "Тушканчики могут обходиться без воды, получая ее из насекомых и семян, и переключаться на животный корм в засуху.",
                        "environment_changes": {"seeds": -80},
                        "feedback_correct": "Тушканчики перешли на насекомых и не пьют воду.",
                        "feedback_incorrect": "В спячке они погибли от голода."
                    },
                    {
                        "description": "Популяция (200 особей) адаптировалась к пустыне.",
                        "choices": [
                            {
                                "text": "Закрепить признаки",
                                "is_correct": True,
                                "effect": {"desert_specialist": 100, "rare_species": "long_eared_jerboa", "viability_index": 40}
                            },
                            {
                                "text": "Расширить рацион",
                                "is_correct": True,
                                "effect": {"diet": 70, "viability_index": 30}
                            },
                            {
                                "text": "Уменьшить уши",
                                "is_correct": False,
                                "effect": {"ears": -50, "viability_index": -40}
                            }
                        ],
                        "scientific_explanation": "Длинноухий тушканчик (Euchoreutes naso) - уникальный вид с экстремально большими ушами, адаптированный к пустыне.",
                        "environment_changes": {},
                        "feedback_correct": "Сформировался вид длинноухих тушканчиков.",
                        "feedback_incorrect": "Уменьшение ушей ухудшило слух."
                    }
                ],
                "initial_population": {
                    "genome_attributes": {
                        "colors": {"sand": 200, "white": 100},
                        "leg_length": 50,
                        "burrowing": 40,
                        "ears": 40,
                        "hearing": 40,
                        "insect_diet": 20
                    },
                    "viability_index": 100,
                    "energy_reserve": 100,
                    "current_environment": {"type": "desert", "temperature": 40, "seeds": 100, "predators": 30}
                },
                "rare_species": ["long_eared_jerboa"]
            },
            {
                "id": "mangrove_fish",
                "title": "🐠 Мангровые рыбы",
                "description": "Адаптация рыб к манграм",
                "stages": [
                    {
                        "description": "Рыбы (400 особей) в манграх. Вода соленая, уровень воды колеблется, мало кислорода.",
                        "choices": [
                            {
                                "text": "Дышать воздухом",
                                "is_correct": True,
                                "effect": {"air_breathing": 80, "viability_index": 40}
                            },
                            {
                                "text": "Жить в воде",
                                "is_correct": False,
                                "effect": {"water_only": 100, "viability_index": -50}
                            },
                            {
                                "text": "Лазать по корням",
                                "is_correct": True,
                                "effect": {"climbing": 70, "viability_index": 35}
                            }
                        ],
                        "scientific_explanation": "Мангровые рыбы (например, илистые прыгуны) могут дышать атмосферным воздухом и передвигаться по суше.",
                        "environment_changes": {"oxygen": -50, "tide": 100},
                        "feedback_correct": "Рыбы научились дышать воздухом и лазать по корням.",
                        "feedback_incorrect": "В воде не хватает кислорода."
                    },
                    {
                        "description": "В воде много крабов, которые поедают икру.",
                        "choices": [
                            {
                                "text": "Икра на суше",
                                "is_correct": True,
                                "effect": {"land_eggs": 80, "viability_index": 45}
                            },
                            {
                                "text": "Живорождение",
                                "is_correct": False,
                                "effect": {"live_birth": 70, "viability_index": -30}
                            },
                            {
                                "text": "Много икры",
                                "is_correct": False,
                                "effect": {"more_eggs": 100, "viability_index": -40}
                            }
                        ],
                        "scientific_explanation": "Некоторые мангровые рыбы откладывают икру на корнях или в норах выше уровня воды, защищая от хищников.",
                        "environment_changes": {"crabs": 60},
                        "feedback_correct": "Икра на суше в безопасности от крабов.",
                        "feedback_incorrect": "Живорождение не развилось."
                    },
                    {
                        "description": "Вода стала очень соленой из-за засухи.",
                        "choices": [
                            {
                                "text": "Солевые железы",
                                "is_correct": True,
                                "effect": {"salt_glands": 80, "viability_index": 40}
                            },
                            {
                                "text": "Пить пресную",
                                "is_correct": False,
                                "effect": {"find_fresh": 100, "viability_index": -30}
                            },
                            {
                                "text": "Мочевой пузырь",
                                "is_correct": True,
                                "effect": {"kidney": 70, "viability_index": 35}
                            }
                        ],
                        "scientific_explanation": "Мангровые рыбы выделяют избыток соли через жабры и почки, поддерживая водно-солевой баланс.",
                        "environment_changes": {"salinity": 200},
                        "feedback_correct": "Рыбы справляются с высокой соленостью.",
                        "feedback_incorrect": "Пресной воды нет."
                    },
                    {
                        "description": "Популяция (250 особей) полностью адаптирована к манграм.",
                        "choices": [
                            {
                                "text": "Закрепить признаки",
                                "is_correct": True,
                                "effect": {"mangrove_specialist": 100, "rare_species": "mudskipper", "viability_index": 40}
                            },
                            {
                                "text": "Вернуться в море",
                                "is_correct": False,
                                "effect": {"sea": 100, "viability_index": -50}
                            },
                            {
                                "text": "Сохранить гибкость",
                                "is_correct": True,
                                "effect": {"flexibility": 70, "viability_index": 30}
                            }
                        ],
                        "scientific_explanation": "Илистые прыгуны (Periophthalmus) - рыбы, полностью адаптированные к жизни в манграх, могут долго находиться на суше.",
                        "environment_changes": {},
                        "feedback_correct": "Сформировалась популяция илистых прыгунов.",
                        "feedback_incorrect": "В море слишком много конкурентов."
                    }
                ],
                "initial_population": {
                    "genome_attributes": {
                        "colors": {"brown": 250, "green": 150},
                        "air_breathing": 20,
                        "climbing": 20,
                        "salt_glands": 30,
                        "kidney": 40
                    },
                    "viability_index": 100,
                    "energy_reserve": 100,
                    "current_environment": {"type": "mangrove", "oxygen": 50, "salinity": 100, "crabs": 40}
                },
                "rare_species": ["mudskipper"]
            },
            {
                "id": "alpine_marmot",
                "title": "🦫 Альпийские сурки",
                "description": "Эволюция сурков в Альпах",
                "stages": [
                    {
                        "description": "Сурки (150 особей) в Альпах на высоте 2000м. Короткое лето, долгая зима.",
                        "choices": [
                            {
                                "text": "Спячка",
                                "is_correct": True,
                                "effect": {"hibernation": 90, "viability_index": 45, "energy_reserve": 50}
                            },
                            {
                                "text": "Запасать корм",
                                "is_correct": False,
                                "effect": {"food_storage": 80, "viability_index": -30}
                            },
                            {
                                "text": "Густой мех",
                                "is_correct": True,
                                "effect": {"fur": 70, "viability_index": 30}
                            }
                        ],
                        "scientific_explanation": "Альпийские сурки (Marmota marmota) впадают в спячку на 6-8 месяцев, снижая метаболизм и температуру тела.",
                        "environment_changes": {"temperature": -10, "winter_length": 8},
                        "feedback_correct": "Сурки впадают в спячку и экономят энергию.",
                        "feedback_incorrect": "Запасов на зиму не хватило."
                    },
                    {
                        "description": "Появились орлы, охотящиеся на сурков.",
                        "choices": [
                            {
                                "text": "Свист-сигнал",
                                "is_correct": True,
                                "effect": {"whistle": 90, "social": 70, "viability_index": 40}
                            },
                            {
                                "text": "Прятаться в норы",
                                "is_correct": True,
                                "effect": {"burrowing": 80, "viability_index": 35}
                            },
                            {
                                "text": "Драться с орлами",
                                "is_correct": False,
                                "effect": {"fight": 100, "viability_index": -60}
                            }
                        ],
                        "scientific_explanation": "Сурки используют громкий свист для предупреждения сородичей об опасности и прячутся в сложные норы.",
                        "environment_changes": {"eagles": 40},
                        "feedback_correct": "Система оповещения помогает спасаться.",
                        "feedback_incorrect": "Против орлов не выстоять."
                    },
                    {
                        "description": "Лето стало короче, нужно быстрее набирать жир.",
                        "choices": [
                            {
                                "text": "Больше есть",
                                "is_correct": True,
                                "effect": {"feeding_rate": 80, "fat": 70, "viability_index": 35}
                            },
                            {
                                "text": "Меньше играть",
                                "is_correct": True,
                                "effect": {"energy_conservation": 70, "viability_index": 30}
                            },
                            {
                                "text": "Спать меньше",
                                "is_correct": False,
                                "effect": {"less_sleep": 100, "viability_index": -40}
                            }
                        ],
                        "scientific_explanation": "Сурки проводят все лето, интенсивно питаясь, чтобы накопить достаточно жира для зимней спячки.",
                        "environment_changes": {"summer": -20},
                        "feedback_correct": "Сурки успевают накопить жир.",
                        "feedback_incorrect": "Недосып снизил активность."
                    },
                    {
                        "description": "Популяция (120 особей) стабильна, хорошо адаптирована.",
                        "choices": [
                            {
                                "text": "Закрепить признаки",
                                "is_correct": True,
                                "effect": {"alpine_specialist": 100, "rare_species": "alpine_marmot", "viability_index": 40}
                            },
                            {
                                "text": "Сократить спячку",
                                "is_correct": False,
                                "effect": {"shorter_hibernation": 100, "viability_index": -50}
                            },
                            {
                                "text": "Сохранить поведение",
                                "is_correct": True,
                                "effect": {"behavior": 80, "viability_index": 30}
                            }
                        ],
                        "scientific_explanation": "Альпийские сурки - классический пример адаптации к сезонному климату через длительную спячку.",
                        "environment_changes": {},
                        "feedback_correct": "Популяция успешно существует.",
                        "feedback_incorrect": "Короткая спячка не спасает от холода."
                    }
                ],
                "initial_population": {
                    "genome_attributes": {
                        "colors": {"brown": 120, "gray": 30},
                        "hibernation": 50,
                        "fur": 50,
                        "whistle": 40,
                        "burrowing": 50,
                        "fat": 40
                    },
                    "viability_index": 100,
                    "energy_reserve": 100,
                    "current_environment": {"type": "alpine", "temperature": 10, "winter_length": 6, "eagles": 20}
                },
                "rare_species": ["alpine_marmot"]
            },
            {
                "id": "snowy_owl",
                "title": "🦉 Полярные совы",
                "description": "Адаптация сов к Арктике",
                "stages": [
                    {
                        "description": "Совы (100 особей) в тундре. Полярный день летом, полярная ночь зимой. Холодно.",
                        "choices": [
                            {
                                "text": "Белое оперение",
                                "is_correct": True,
                                "effect": {"white_feathers": 80, "camouflage": 80, "viability_index": 35}
                            },
                            {
                                "text": "Ночная охота",
                                "is_correct": False,
                                "effect": {"night_hunting": 100, "viability_index": -30}
                            },
                            {
                                "text": "Густой пух",
                                "is_correct": True,
                                "effect": {"down": 80, "viability_index": 30}
                            }
                        ],
                        "scientific_explanation": "Полярные совы (Bubo scandiacus) имеют белое оперение для маскировки на снегу и густой пух для теплоизоляции.",
                        "environment_changes": {"temperature": -20, "daylight": 0},
                        "feedback_correct": "Белые совы незаметны на снегу и не мерзнут.",
                        "feedback_incorrect": "Ночью не видно добычу."
                    },
                    {
                        "description": "Основная добыча - лемминги. Их численность сильно колеблется.",
                        "choices": [
                            {
                                "text": "Охотиться на зайцев",
                                "is_correct": True,
                                "effect": {"hare_hunting": 70, "viability_index": 35}
                            },
                            {
                                "text": "Кочевать",
                                "is_correct": True,
                                "effect": {"nomadic": 80, "viability_index": 30}
                            },
                            {
                                "text": "Меньше есть",
                                "is_correct": False,
                                "effect": {"eat_less": 100, "viability_index": -50}
                            }
                        ],
                        "scientific_explanation": "При нехватке леммингов полярные совы могут охотиться на зайцев, птиц и кочевать в поисках пищи.",
                        "environment_changes": {"lemmings": -70},
                        "feedback_correct": "Совы переключились на зайцев и кочуют.",
                        "feedback_incorrect": "Голод привел к гибели."
                    },
                    {
                        "description": "Изменение климата: зимы стали теплее, снега меньше.",
                        "choices": [
                            {
                                "text": "Темные перья",
                                "is_correct": True,
                                "effect": {"darker_feathers": 60, "camouflage": 40, "viability_index": 30}
                            },
                            {
                                "text": "Остаться белыми",
                                "is_correct": False,
                                "effect": {"white": 100, "viability_index": -40}
                            },
                            {
                                "text": "Смешанный окрас",
                                "is_correct": True,
                                "effect": {"mixed_color": 70, "viability_index": 35}
                            }
                        ],
                        "scientific_explanation": "При сокращении снежного покрова темные особи получают преимущество, так как лучше маскируются на бурой земле.",
                        "environment_changes": {"snow": -50},
                        "feedback_correct": "Более темные совы лучше маскируются.",
                        "feedback_incorrect": "Белые совы на бурой земле заметны."
                    },
                    {
                        "description": "Популяция (80 особей) адаптировалась к новым условиям.",
                        "choices": [
                            {
                                "text": "Закрепить окрас",
                                "is_correct": True,
                                "effect": {"arctic_specialist": 100, "rare_species": "snowy_owl", "viability_index": 40}
                            },
                            {
                                "text": "Мигрировать на север",
                                "is_correct": False,
                                "effect": {"migration": 100, "viability_index": -30}
                            },
                            {
                                "text": "Сохранить изменчивость",
                                "is_correct": True,
                                "effect": {"variability": 70, "viability_index": 30}
                            }
                        ],
                        "scientific_explanation": "Полярные совы демонстрируют адаптивную изменчивость окраски в зависимости от условий.",
                        "environment_changes": {},
                        "feedback_correct": "Популяция адаптировалась к изменениям.",
                        "feedback_incorrect": "Миграция в никуда не помогла."
                    }
                ],
                "initial_population": {
                    "genome_attributes": {
                        "colors": {"white": 80, "spotted": 20},
                        "white_feathers": 80,
                        "down": 60,
                        "hare_hunting": 30,
                        "nomadic": 40
                    },
                    "viability_index": 100,
                    "energy_reserve": 100,
                    "current_environment": {"type": "arctic", "temperature": -20, "snow": 80, "lemmings": 100}
                },
                "rare_species": ["snowy_owl"]
            }
        ],
        "species": {
            "city_tit": {
                "name": "Синица городская",
                "description": "Адаптирована к жизни в городе, использует кормушки",
                "emoji": "🐦"
            },
            "sand_gecko": {
                "name": "Геккон песчаный",
                "description": "Ночной, быстро бегает по песку, отбрасывает хвост",
                "emoji": "🦎"
            },
            "cave_astyanax": {
                "name": "Астианакс пещерный",
                "description": "Слепая пещерная рыба с развитой боковой линией",
                "emoji": "🐟"
            },
            "gray_fox": {
                "name": "Песец серый",
                "description": "Серая зимняя морфа, адаптирована к малоснежным зимам",
                "emoji": "🦊"
            },
            "island_rat": {
                "name": "Крыса островная",
                "description": "Крупная, древесная, с разделением пищевых ниш",
                "emoji": "🐀"
            },
            "alpine_ibex": {
                "name": "Козел альпийский",
                "description": "Отлично лазает по скалам, большие легкие",
                "emoji": "🐐"
            },
            "long_eared_jerboa": {
                "name": "Тушканчик длинноухий",
                "description": "Огромные уши, отличный слух, не пьет воду",
                "emoji": "🐭"
            },
            "mudskipper": {
                "name": "Прыгун илистый",
                "description": "Дышит воздухом, лазает по корням, откладывает икру на суше",
                "emoji": "🐠"
            },
            "alpine_marmot": {
                "name": "Сурок альпийский",
                "description": "Впадает в спячку на 8 месяцев, свистит при опасности",
                "emoji": "🦫"
            },
            "snowy_owl": {
                "name": "Сова полярная",
                "description": "Белое оперение, адаптивный окрас, кочует за добычей",
                "emoji": "🦉"
            }
        }
    }
    
    os.makedirs('data', exist_ok=True)
    with open('data/content_bank.json', 'w', encoding='utf-8') as f:
        json.dump(bank, f, ensure_ascii=False, indent=2)
    
    print("✅ Создан банк из 10 сценариев по 4 этапа")
    print("📊 Сценариев:", len(bank["scenarios"]))
    for s in bank["scenarios"]:
        print(f"   • {s['title']} - {len(s['stages'])} этапов")
    print("🧬 Видов:", len(bank["species"]))

if __name__ == "__main__":
    create_final_bank()
