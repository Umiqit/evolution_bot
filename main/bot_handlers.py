import logging
import sys
from typing import Dict, List, Optional, Tuple, Any
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler, 
    ConversationHandler, ContextTypes
)
import random
from datetime import datetime

MAIN_MENU, SIMULATION_ACTIVE, WAITING_CHOICE, SCENARIO_SELECT = range(4)

class EvolutionBot:
    def __init__(self, data_storage, scenario_generator):
        self.data_storage = data_storage
        self.scenario_generator = scenario_generator
        self.user_objects = {}
        self.population_objects = {}
    
    def get_user(self, user_id: int, username: str = "", first_name: str = ""):
        if user_id not in self.user_objects:
            user_data = self.data_storage.get_user(user_id)
            if not user_data.get("username") and username:
                user_data["username"] = username
            if not user_data.get("first_name") and first_name:
                user_data["first_name"] = first_name
            from database import User
            user = User.from_dict(user_data)
            self.user_objects[user_id] = user
        return self.user_objects[user_id]
    
    def save_user(self, user_id: int):
        if user_id in self.user_objects:
            user = self.user_objects[user_id]
            self.data_storage.update_user(user_id, user.to_dict())
    
    def create_inline_keyboard(self, buttons_data: List[Tuple[str, str]]) -> InlineKeyboardMarkup:
        keyboard = []
        for text, callback_data in buttons_data:
            keyboard.append([InlineKeyboardButton(text, callback_data=callback_data)])
        return InlineKeyboardMarkup(keyboard)
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        user = update.effective_user
        db_user = self.get_user(user.id, user.username or "", user.first_name or "")
        
        welcome_text = (
            f"👋 Привет, {user.first_name}!\n\n"
            f"Это игра про эволюцию. Твоя задача - проводить популяции через разные сценарии.\n"
            f"Выбирай стратегии, собирай виды и повышай свой ранг.\n\n"
            f"Используй меню для навигации."
        )
        
        await self.show_main_menu(update, context, db_user, welcome_text)
        return MAIN_MENU
    
    async def show_main_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE, 
                            user, extra_text: str = ""):
        status_text = (
            f"👤 {user.first_name or 'Куратор'}\n"
            f"📊 Ранг: {user.status_level} | Уровень: {user.progress_level}\n"
            f"✨ Опыт: {user.experience}\n"
            f"📋 Сценариев: {len(user.completed_scenarios)}/{self.scenario_generator.get_scenario_count()}\n"
            f"🧬 Видов: {len(user.collected_species)}\n"
            f"🏆 Достижений: {len(user.achievements_unlocked)}"
        )
        
        if extra_text:
            main_text = extra_text + "\n\n" + status_text
        else:
            main_text = "📋 Главное меню\n\n" + status_text
        
        buttons = [
            ("🆕 Новая игра", "new_game"),
            ("📊 Статус", "status"),
            ("📦 Инвентарь", "inventory"),
            ("🏆 Достижения", "achievements"),
            ("❓ Помощь", "help")
        ]
        
        reply_markup = self.create_inline_keyboard(buttons)
        
        if update.callback_query:
            await update.callback_query.edit_message_text(
                main_text, reply_markup=reply_markup
            )
        else:
            await update.message.reply_text(
                main_text, reply_markup=reply_markup
            )
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        help_text = (
            "❓ Помощь по игре\n\n"
            "📋 Команды:\n"
            "/start - Главное меню\n"
            "/help - Эта справка\n"
            "/status - Статус популяции\n"
            "/inventory - Коллекция видов\n"
            "/next - Следующий этап (в игре)\n\n"
            "🎮 Как играть:\n"
            "1. Начни новую игру из меню\n"
            "2. На каждом этапе выбирай вариант развития\n"
            "3. Следи за параметрами популяции\n"
            "4. Собирай редкие виды\n\n"
            "👑 Ранги:\n"
            "Наблюдатель (0+ опыта)\n"
            "Адаптатор (100+ опыта)\n"
            "Архитектор биосферы (300+ опыта)\n"
            "Творец эволюции (600+ опыта)"
        )
        
        buttons = [("🔙 В меню", "main_menu")]
        reply_markup = self.create_inline_keyboard(buttons)
        
        if update.callback_query:
            await update.callback_query.edit_message_text(
                help_text, reply_markup=reply_markup
            )
        else:
            await update.message.reply_text(
                help_text, reply_markup=reply_markup
            )
        return MAIN_MENU
    
    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        user = update.effective_user
        db_user = self.get_user(user.id)
        
        if update.callback_query:
            query = update.callback_query
            await query.answer()
            reply_func = query.edit_message_text
        else:
            reply_func = update.message.reply_text
        
        if db_user.state == "simulation_active" and db_user.current_population:
            if user.id not in self.population_objects:
                from generator import Population
                population = Population.from_dict(db_user.current_population)
                self.population_objects[user.id] = population
            else:
                population = self.population_objects[user.id]
            
            scenario = self.scenario_generator.get_scenario_by_id(db_user.current_scenario_id)
            scenario_name = scenario.get('title', 'Неизвестно') if scenario else 'Неизвестно'
            stages_count = len(scenario.get('stages', [])) if scenario else 0
            
            status_text = (
                f"📊 Текущая эволюция\n\n"
                f"Сценарий: {scenario_name}\n"
                f"Этап: {db_user.current_stage + 1}/{stages_count}\n\n"
                f"Жизнеспособность: {population.viability_index:.1f}%\n"
                f"Энергия: {population.energy_reserve:.1f}\n\n"
                f"Генетические признаки:\n"
            )
            
            colors = population.genome_attributes.get("colors", {})
            if colors:
                for color, count in colors.items():
                    status_text += f"  • {color}: {count}\n"
            
            for attr in ["speed", "camouflage", "beak_size", "diet_diversity", "cold_resistance", 
                        "synanthropy", "nocturnal", "burrowing", "tail_autotomy", "lung_capacity",
                        "climbing", "herd", "ears", "hearing", "air_breathing", "hibernation"]:
                if attr in population.genome_attributes:
                    status_text += f"  • {attr}: {population.genome_attributes[attr]}\n"
            
            buttons = [
                ("▶️ Продолжить", "continue_simulation"),
                ("🔙 В меню", "main_menu")
            ]
        else:
            status_text = (
                f"📊 Статус игрока\n\n"
                f"Ранг: {db_user.status_level}\n"
                f"Уровень: {db_user.progress_level}\n"
                f"Опыт: {db_user.experience}\n\n"
                f"Пройдено сценариев: {len(db_user.completed_scenarios)}/{self.scenario_generator.get_scenario_count()}\n"
                f"Собрано видов: {len(db_user.collected_species)}\n"
                f"Достижений: {len(db_user.achievements_unlocked)}"
            )
            
            buttons = [("🔙 В меню", "main_menu")]
        
        reply_markup = self.create_inline_keyboard(buttons)
        await reply_func(status_text, reply_markup=reply_markup)
        
        return MAIN_MENU if db_user.state != "simulation_active" else SIMULATION_ACTIVE
    
    async def inventory_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        user = update.effective_user
        db_user = self.get_user(user.id)
        
        if update.callback_query:
            query = update.callback_query
            await query.answer()
            reply_func = query.edit_message_text
        else:
            reply_func = update.message.reply_text
        
        if not db_user.collected_species:
            inventory_text = "📦 Инвентарь\n\nУ вас пока нет собранных видов."
        else:
            inventory_text = f"📦 Инвентарь\n\nВсего видов: {len(db_user.collected_species)}\n\n"
            
            for species_id in db_user.collected_species:
                species = self.scenario_generator.get_species_info(species_id)
                if species:
                    inventory_text += f"• {species.get('emoji', '🔹')} {species.get('name', species_id)}\n"
                else:
                    inventory_text += f"• {species_id}\n"
        
        buttons = [("🔙 В меню", "main_menu")]
        reply_markup = self.create_inline_keyboard(buttons)
        await reply_func(inventory_text, reply_markup=reply_markup)
        
        return MAIN_MENU
    
    async def achievements_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        user = update.effective_user
        db_user = self.get_user(user.id)
        
        if update.callback_query:
            query = update.callback_query
            await query.answer()
            reply_func = query.edit_message_text
        else:
            reply_func = update.message.reply_text
        
        from database import AchievementSystem
        
        achievements_text = "🏆 Достижения\n\n"
        
        if not db_user.achievements_unlocked:
            achievements_text += "У вас пока нет достижений."
        else:
            for ach_id in db_user.achievements_unlocked:
                ach_data = AchievementSystem.ACHIEVEMENTS.get(ach_id, {})
                achievements_text += f"✅ {ach_data.get('name', ach_id)}\n"
                achievements_text += f"   {ach_data.get('description', '')}\n\n"
        
        buttons = [("🔙 В меню", "main_menu")]
        reply_markup = self.create_inline_keyboard(buttons)
        await reply_func(achievements_text, reply_markup=reply_markup)
        
        return MAIN_MENU
    
    async def new_game(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        db_user = self.get_user(user_id)
        
        if db_user.state == "simulation_active" and db_user.current_scenario_id:
            scenario = self.scenario_generator.get_scenario_by_id(db_user.current_scenario_id)
            scenario_name = scenario.get('title', 'Неизвестно') if scenario else 'Неизвестно'
            stage_num = db_user.current_stage + 1
            stages_total = len(scenario.get('stages', [])) if scenario else 0
            
            text = (
                f"⚠️ У вас есть незавершенная эволюция!\n\n"
                f"Сценарий: {scenario_name}\n"
                f"Этап: {stage_num}/{stages_total}\n\n"
                f"Что делаем?"
            )
            
            buttons = [
                ("▶️ Продолжить", "continue_simulation"),
                ("🆕 Выбрать новый", "show_scenarios"),
                ("🔙 В меню", "main_menu")
            ]
            reply_markup = self.create_inline_keyboard(buttons)
            await query.edit_message_text(text, reply_markup=reply_markup)
            return MAIN_MENU
        
        await self.show_scenario_selection(update, context, db_user)
        return SCENARIO_SELECT
    
    async def force_new_game(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        db_user = self.get_user(user_id)
        
        if db_user.state == "simulation_active":
            db_user.finish_simulation()
            if user_id in self.population_objects:
                del self.population_objects[user_id]
            self.save_user(user_id)
        
        await self.show_scenario_selection(update, context, db_user)
        return SCENARIO_SELECT
    
    async def show_scenario_selection(self, update: Update, context: ContextTypes.DEFAULT_TYPE, user):
        query = update.callback_query
        
        all_scenarios = self.scenario_generator.get_all_scenarios()
        completed = user.completed_scenarios
        
        available = []
        for s in all_scenarios:
            if s.get('id') not in completed:
                available.append(s)
        
        if not available:
            text = "🎉 Вы прошли все доступные сценарии!\n\nСледите за обновлениями - скоро появятся новые."
            buttons = [("🔙 В меню", "main_menu")]
            reply_markup = self.create_inline_keyboard(buttons)
            await query.edit_message_text(text, reply_markup=reply_markup)
            return MAIN_MENU
        
        text = "🎮 Выберите сценарий для эволюции:\n\n"
        
        buttons = []
        for s in available[:10]:
            emoji = s.get('title', '')[0] if s.get('title') else '🌍'
            buttons.append((f"{emoji} {s.get('title', 'Неизвестно')}", f"select_{s.get('id')}"))
        
        buttons.append(("🔙 В меню", "main_menu"))
        
        reply_markup = self.create_inline_keyboard(buttons)
        await query.edit_message_text(text, reply_markup=reply_markup)
    
    async def select_scenario(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        query = update.callback_query
        await query.answer()
        
        scenario_id = query.data.replace("select_", "")
        user_id = query.from_user.id
        db_user = self.get_user(user_id)
        
        if db_user.state == "simulation_active":
            db_user.finish_simulation()
            if user_id in self.population_objects:
                del self.population_objects[user_id]
        
        scenario = self.scenario_generator.get_scenario_by_id(scenario_id)
        if not scenario:
            await query.edit_message_text("Ошибка: сценарий не найден.")
            return MAIN_MENU
        
        initial_population = self.scenario_generator.get_initial_population(scenario_id)
        db_user.start_new_simulation(scenario_id, initial_population)
        
        from generator import Population
        self.population_objects[user_id] = Population.from_dict(initial_population)
        self.save_user(user_id)
        
        await self.show_stage(query, context, db_user)
        return WAITING_CHOICE
    
    async def show_stage(self, query, context: ContextTypes.DEFAULT_TYPE, user):
        scenario = self.scenario_generator.get_scenario_by_id(user.current_scenario_id)
        if not scenario:
            await query.edit_message_text("Ошибка: сценарий не найден.")
            return
        
        stage_data = self.scenario_generator.get_stage_data(user.current_scenario_id, user.current_stage)
        if not stage_data:
            await self.finish_scenario(query, context, user)
            return
        
        from generator import SimulationStep
        step = SimulationStep(stage_data)
        text, choices = step.render()
        
        text = text.replace('*', '').replace('_', '').replace('`', '')
        
        if user.user_id in self.population_objects:
            population = self.population_objects[user.user_id]
            population_info = (
                f"\n\n[Жизн: {population.viability_index:.0f}% | "
                f"Энер: {population.energy_reserve:.0f}]"
            )
        else:
            population_info = ""
        
        stage_info = f"{scenario.get('title')} - Этап {user.current_stage + 1}/{len(scenario.get('stages', []))}\n\n"
        full_text = stage_info + text + population_info
        
        buttons = []
        for i, choice_text in enumerate(choices):
            short_text = choice_text[:25] + "..." if len(choice_text) > 25 else choice_text
            buttons.append((f"{i+1}. {short_text}", f"choice_{i}"))
        
        buttons.append(("❌ Прервать", "abort_simulation"))
        
        reply_markup = self.create_inline_keyboard(buttons)
        
        await query.edit_message_text(
            full_text,
            reply_markup=reply_markup
        )
        
        user.state = "waiting_choice"
        self.save_user(user.user_id)
    
    async def process_choice(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        db_user = self.get_user(user_id)
        
        if db_user.state != "waiting_choice":
            return MAIN_MENU
        
        choice_index = int(query.data.split("_")[1])
        
        scenario = self.scenario_generator.get_scenario_by_id(db_user.current_scenario_id)
        stage_data = self.scenario_generator.get_stage_data(db_user.current_scenario_id, db_user.current_stage)
        
        from generator import SimulationStep
        step = SimulationStep(stage_data)
        result = step.process_choice(choice_index)
        
        if user_id in self.population_objects:
            population = self.population_objects[user_id]
        else:
            from generator import Population
            population = Population.from_dict(db_user.current_population)
            self.population_objects[user_id] = population
        
        old_viability = population.viability_index
        old_energy = population.energy_reserve
        
        population.apply_effects(result.get("effect", {}))
        db_user.current_population = population.to_dict()
        
        viability_change = population.viability_index - old_viability
        energy_change = population.energy_reserve - old_energy
        
        reward = None
        if result.get("is_correct", False) and db_user.current_stage == len(scenario.get("stages", [])) - 1:
            rare_species = scenario.get("rare_species", [])
            if rare_species and random.random() < 0.3:
                reward = random.choice(rare_species)
        
        if reward and reward not in db_user.collected_species:
            db_user.add_species(reward)
        
        exp_gain = 10 if result.get("is_correct", False) else 2
        db_user.update_progress(exp_gain)
        
        self.save_user(user_id)
        
        result_text = f"{result.get('feedback', '')}\n\n"
        result_text += f"📊 Изменения:\n"
        result_text += f"   Жизнеспособность: {old_viability:.0f} → {population.viability_index:.0f} "
        if viability_change > 0:
            result_text += f"(+{viability_change:.0f})\n"
        else:
            result_text += f"({viability_change:.0f})\n"
        
        result_text += f"   Энергия: {old_energy:.0f} → {population.energy_reserve:.0f} "
        if energy_change > 0:
            result_text += f"(+{energy_change:.0f})\n"
        else:
            result_text += f"({energy_change:.0f})\n"
        
        if result.get('scientific_explanation'):
            result_text += f"\n🔬 {result.get('scientific_explanation')}\n"
        
        if reward:
            species_info = self.scenario_generator.get_species_info(reward)
            if species_info:
                result_text += f"\n🎉 ПОЛУЧЕН НОВЫЙ ВИД: {species_info.get('name', reward)} {species_info.get('emoji', '')}\n"
                result_text += f"   {species_info.get('description', '')}\n"
        else:
            if db_user.current_stage == len(scenario.get("stages", [])) - 1:
                result_text += f"\n⏳ Вид не получен. Попробуйте пройти сценарий снова с другим выбором.\n"
        
        result_text += f"\n✨ Опыт: +{exp_gain}"
        
        if population.is_extinct():
            result_text += "\n\n💀 Популяция вымерла! Эволюция прервана."
            db_user.finish_simulation()
            if user_id in self.population_objects:
                del self.population_objects[user_id]
            self.save_user(user_id)
            
            buttons = [
                ("🆕 Новая игра", "new_game"),
                ("🔙 В меню", "main_menu")
            ]
            reply_markup = self.create_inline_keyboard(buttons)
            await query.edit_message_text(result_text, reply_markup=reply_markup)
            return MAIN_MENU
        
        db_user.current_stage += 1
        db_user.state = "simulation_active"
        self.save_user(user_id)
        
        if db_user.current_stage >= len(scenario.get("stages", [])):
            result_text += "\n\n✅ Сценарий пройден! Нажмите для завершения."
            buttons = [("✅ Завершить", "finish_scenario")]
        else:
            buttons = [("▶️ Дальше", "next_stage")]
        
        reply_markup = self.create_inline_keyboard(buttons)
        await query.edit_message_text(result_text, reply_markup=reply_markup)
        return SIMULATION_ACTIVE
    
    async def finish_scenario(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        db_user = self.get_user(user_id)
        
        if db_user.current_scenario_id and db_user.current_scenario_id not in db_user.completed_scenarios:
            db_user.completed_scenarios.append(db_user.current_scenario_id)
        
        db_user.finish_simulation()
        if user_id in self.population_objects:
            del self.population_objects[user_id]
        
        from database import AchievementSystem
        new_achievements = AchievementSystem.check_achievements(db_user)
        
        db_user.update_progress(50)
        self.save_user(user_id)
        
        text = "✅ Сценарий пройден! +50 опыта"
        
        if new_achievements:
            text += "\n\n🏆 Новые достижения:\n"
            for ach in new_achievements:
                text += f"• {ach}\n"
        
        buttons = [
            ("🆕 Новый сценарий", "new_game"),
            ("🔙 В меню", "main_menu")
        ]
        reply_markup = self.create_inline_keyboard(buttons)
        
        await query.edit_message_text(text, reply_markup=reply_markup)
        return MAIN_MENU
    
    async def continue_simulation(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        db_user = self.get_user(user_id)
        
        if db_user.state != "simulation_active":
            await self.show_main_menu(update, context, db_user)
            return MAIN_MENU
        
        await self.show_stage(query, context, db_user)
        return WAITING_CHOICE
    
    async def next_stage(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        db_user = self.get_user(user_id)
        
        if db_user.state != "simulation_active":
            await self.show_main_menu(update, context, db_user)
            return MAIN_MENU
        
        if not db_user.current_scenario_id:
            await self.show_main_menu(update, context, db_user)
            return MAIN_MENU
        
        await self.show_stage(query, context, db_user)
        return WAITING_CHOICE
    
    async def abort_simulation(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        db_user = self.get_user(user_id)
        
        db_user.finish_simulation()
        if user_id in self.population_objects:
            del self.population_objects[user_id]
        self.save_user(user_id)
        
        await query.edit_message_text("❌ Эволюция прервана.")
        await self.show_main_menu(update, context, db_user)
        return MAIN_MENU
    
    async def button_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        query = update.callback_query
        await query.answer()
        
        data = query.data
        user_id = query.from_user.id
        db_user = self.get_user(user_id)
        
        if data == "main_menu":
            await self.show_main_menu(update, context, db_user)
            return MAIN_MENU
        elif data == "new_game":
            return await self.new_game(update, context)
        elif data == "show_scenarios":
            await self.show_scenario_selection(update, context, db_user)
            return SCENARIO_SELECT
        elif data == "force_new_game":
            return await self.force_new_game(update, context)
        elif data == "status":
            return await self.status_command(update, context)
        elif data == "inventory":
            return await self.inventory_command(update, context)
        elif data == "achievements":
            return await self.achievements_command(update, context)
        elif data == "help":
            return await self.help_command(update, context)
        elif data == "continue_simulation":
            return await self.continue_simulation(update, context)
        elif data == "next_stage":
            return await self.next_stage(update, context)
        elif data == "finish_scenario":
            return await self.finish_scenario(update, context)
        elif data == "abort_simulation":
            return await self.abort_simulation(update, context)
        elif data.startswith("select_"):
            return await self.select_scenario(update, context)
        elif data.startswith("choice_"):
            return await self.process_choice(update, context)
        
        return MAIN_MENU
    
    async def next_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        user = update.effective_user
        db_user = self.get_user(user.id)
        
        if db_user.state != "simulation_active":
            await update.message.reply_text("Сейчас нет активной игры. Начните новую из меню.")
            return MAIN_MENU
        
        class TempQuery:
            def __init__(self, user_id, message):
                self.from_user = type('obj', (), {'id': user_id})
                self.message = message
            async def edit_message_text(self, text, reply_markup=None, parse_mode=None):
                await self.message.reply_text(text, reply_markup=reply_markup)
        
        temp_query = TempQuery(user.id, update.message)
        await self.show_stage(temp_query, context, db_user)
        return WAITING_CHOICE
