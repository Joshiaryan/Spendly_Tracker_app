import flet as ft
from datetime import datetime

# This class handles the app logic and UI building
class SpendlyApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Spendly - NRS Expense Tracker"
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.window_width = 400
        self.page.window_height = 800
        self.page.bgcolor = "#F8FAFC"
        
        # Application State
        self.transactions = []
        self.total_balance = 0.0
        self.total_income = 0.0
        self.total_expenses = 0.0
        
        # Sub-category definitions
        self.sub_categories = {
            "Food": [("Veg", "🥦"), ("Meat", "🥩"), ("Dal", "🥣"), ("Drink", "🥤")],
            "Shopping": [("Clothes", "👕"), ("Gadget", "📱"), ("Home", "🏠"), ("Gift", "🎁")],
            "Transport": [("Fuel", "⛽"), ("Bus", "🚌"), ("Taxi", "🚕"), ("Bike", "🏍️")],
            "Income": [("Salary", "💵"), ("Bonus", "🧧"), ("Other", "💎")]
        }
        
        self.selected_main_cat = "Food"
        self.selected_sub_cat = "Dal"
        
        self.init_ui()

    def create_nav_item(self, icon, label, selected=False):
        color = "#4F46E5" if selected else "#94A3B8"
        return ft.Column(
            controls=[
                ft.Icon(icon, color=color, size=24),
                ft.Text(label, size=10, color=color, weight=ft.FontWeight.BOLD)
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=4
        )

    def update_totals(self):
        self.total_income = sum(t['amount'] for t in self.transactions if t['type'] == "Income")
        self.total_expenses = sum(t['amount'] for t in self.transactions if t['type'] == "Expense")
        self.total_balance = self.total_income - self.total_expenses
        
        self.balance_text.value = f"Rs. {self.total_balance:,.0f}"
        self.income_text.value = f"Rs. {self.total_income:,.0f}"
        self.expense_text.value = f"Rs. {self.total_expenses:,.0f}"
        self.page.update()

    def init_ui(self):
        # UI Elements for updates
        self.balance_text = ft.Text("Rs. 0", size=32, weight=ft.FontWeight.BOLD, color="white")
        self.income_text = ft.Text("Rs. 0", size=14, weight=ft.FontWeight.BOLD, color="white")
        self.expense_text = ft.Text("Rs. 0", size=14, weight=ft.FontWeight.BOLD, color="white")
        self.transaction_list = ft.Column(spacing=10, scroll=ft.ScrollMode.HIDDEN)

        # Main Balance Card
        balance_card = ft.Container(
            content=ft.Column([
                ft.Text("Total Balance", color="#C7D2FE", size=14),
                self.balance_text,
                ft.Row([
                    ft.Row([
                        ft.Container(ft.Icon(ft.icons.Icons.ARROW_DOWNWARD, color="white", size=16), bgcolor="white10", border_radius=20, padding=5),
                        ft.Column([ft.Text("INCOME", size=10, color="#C7D2FE"), self.income_text], spacing=0)
                    ]),
                    ft.Row([
                        ft.Container(ft.Icon(ft.icons.Icons.ARROW_UPWARD, color="white", size=16), bgcolor="white10", border_radius=20, padding=5),
                        ft.Column([ft.Text("EXPENSES", size=10, color="#C7D2FE"), self.expense_text], spacing=0)
                    ])
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
            ]),
            padding=30,
            bgcolor="#4F46E5",
            border_radius=30,
            shadow=ft.BoxShadow(blur_radius=20, color="#4F46E544")
        )

        self.main_container = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Column([ft.Text("Namaste,", color="#64748B"), ft.Text("Alex Rivers", size=20, weight="bold")]),
                    ft.CircleAvatar(content=ft.Text("AR"), bgcolor="#4F46E5", color="white")
                ], alignment="spaceBetween"),
                ft.Divider(height=10, color="transparent"),
                balance_card,
                ft.Divider(height=20, color="transparent"),
                ft.Row([ft.Text("Recent Activities", size=18, weight="bold"), ft.Text("View All", color="#4F46E5", size=12)]),
                self.transaction_list
            ], scroll=ft.ScrollMode.HIDDEN),
            expand=True,
            padding=20
        )

        # Add Button (FAB)
        fab = ft.FloatingActionButton(
            icon=ft.icons.Icons.ADD,
            bgcolor="#4F46E5",
            on_click=self.show_add_modal,
            shape=ft.RoundedRectangleBorder(radius=15)
        )

        self.page.add(self.main_container)
        self.page.floating_action_button = fab
        self.page.update()

    def show_add_modal(self, e):
        amount_input = ft.TextField(label="Amount (Rs.)", prefix="Rs. ", text_size=20, border_radius=15, keyboard_type=ft.KeyboardType.NUMBER)
        desc_input = ft.TextField(label="What was this for?", border_radius=15)
        
        # Sub-category grid logic
        sub_cat_row = ft.Row(scroll=ft.ScrollMode.ALWAYS)
        
        def update_subs(cat_name):
            self.selected_main_cat = cat_name
            sub_cat_row.controls.clear()
            for name, icon in self.sub_categories[cat_name]:
                def select_sub(e, n=name):
                    self.selected_sub_cat = n
                    self.page.snack_bar = ft.SnackBar(ft.Text(f"Selected {n}"))
                    self.page.snack_bar.open = True
                    self.page.update()

                sub_cat_row.controls.append(
                    ft.Container(
                        content=ft.Column([
                            ft.Text(icon, size=24),
                            ft.Text(name, size=10, weight="bold")
                        ], horizontal_alignment="center"),
                        bgcolor="#F1F5F9",
                        padding=10,
                        border_radius=15,
                        width=70,
                        on_click=select_sub
                    )
                )
            self.page.update()

        # Category selection buttons
        cat_selector = ft.Row([
            ft.IconButton(ft.icons.Icons.RESTAURANT, on_click=lambda _: update_subs("Food"), icon_color="#F59E0B"),
            ft.IconButton(ft.icons.Icons.SHOPPING_BAG, on_click=lambda _: update_subs("Shopping"), icon_color="#3B82F6"),
            ft.IconButton(ft.icons.Icons.DIRECTIONS_CAR, on_click=lambda _: update_subs("Transport"), icon_color="#10B981"),
            ft.IconButton(ft.icons.Icons.ATTACH_MONEY, on_click=lambda _: update_subs("Income"), icon_color="#4F46E5"),
        ], alignment="center")

        def save_clicked(e):
            if not amount_input.value: return
            
            is_income = self.selected_main_cat == "Income"
            new_trans = {
                "amount": float(amount_input.value),
                "desc": desc_input.value or self.selected_sub_cat,
                "type": "Income" if is_income else "Expense",
                "cat": f"{self.selected_main_cat} • {self.selected_sub_cat}",
                "date": datetime.now().strftime("%d %b")
            }
            
            self.transactions.insert(0, new_trans)
            self.render_transactions()
            self.update_totals()
            bs.open = False
            self.page.update()

        bs_content = ft.Container(
            content=ft.Column([
                ft.Container(width=40, height=5, bgcolor="#E2E8F0", border_radius=10, margin=ft.margin.Margin(bottom=20)),
                ft.Text("Add Transaction", size=20, weight="bold"),
                amount_input,
                desc_input,
                ft.Text("Select Category", size=12, weight="bold", color="#94A3B8"),
                cat_selector,
                sub_cat_row,
                ft.Button("Save Transaction", bgcolor="#4F46E5", color="white", width=400, height=50, on_click=save_clicked),
                ft.Divider(height=20, color="transparent")
            ], horizontal_alignment="center", spacing=15),
            padding=30,
            bgcolor="white",
            border_radius=ft.border_radius.BorderRadius(30, 30, 0, 0)
        )

        bs = ft.BottomSheet(content=bs_content, open=True)
        self.page.overlay.append(bs)
        update_subs("Food") # Default load
        self.page.update()

    def render_transactions(self):
        self.transaction_list.controls.clear()
        for t in self.transactions:
            color = "#10B981" if t['type'] == "Income" else "#EF4444"
            prefix = "+" if t['type'] == "Income" else "-"
            
            self.transaction_list.controls.append(
                ft.Container(
                    content=ft.Row([
                        ft.Row([
                            ft.Container(ft.Icon(ft.icons.Icons.RECEIPT_LONG, color="#4F46E5"), bgcolor="#EEF2FF", border_radius=12, padding=12),
                            ft.Column([
                                ft.Text(t['desc'], weight="bold", size=14),
                                ft.Text(t['cat'], size=11, color="#94A3B8")
                            ], spacing=2)
                        ]),
                        ft.Column([
                            ft.Text(f"{prefix}Rs. {t['amount']:,.0f}", weight="bold", color=color, size=14),
                            ft.Text(t['date'], size=10, color="#94A3B8")
                        ], horizontal_alignment="end")
                    ], alignment="spaceBetween"),
                    padding=15,
                    bgcolor="white",
                    border_radius=20,
                    border=ft.border.all(1, "#F1F5F9")
                )
            )
        self.page.update()

if __name__ == "__main__":
    def main(page: ft.Page):
        SpendlyApp(page)

    ft.run(main)