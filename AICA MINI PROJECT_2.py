"""
College Enquiry Chatbot - Rule-Based AI with Tkinter GUI (single file)
Run:  python chatbot.py
"""
import re
import tkinter as tk
from tkinter import scrolledtext
from datetime import datetime

# =====================================================================
# 1. KNOWLEDGE BASE  (you can modify this for your college)
# =====================================================================
COLLEGE_NAME = "CHAROTAR VIDHYA MANDAL UNIVERSITY"

RULES = [
    {"intent": "greeting",
     "keywords": ["hi", "hello", "hey", "good morning", "good evening", "namaste"],
     "response": f"Hello! Welcome to {COLLEGE_NAME}.\nAsk me about admissions, courses, "
                 "fees, hostel, library, placements, timings or contact details."},
    {"intent": "courses",
     "keywords": ["course", "courses", "program", "programs", "degree", "stream",
                  "bsc", "bcom", "bca", "ba", "mca", "mcom", "branch"],
     "response": "We offer these programs:\n"
                "• B.Tech (Computer Science, Information Technology, Electrical Engineering, mechanical Engineering, Civil Engineering, Electronics Engineering)\n"
                 "• B.Sc. (Computer Science, Maths, Physics, Chemistry)\n"
                 "• B.Com. (General, Accounting & Finance)\n"
                 "• BCA (Bachelor of Computer Applications)\n"
                 "• BA (English, Economics, Psychology)\n"
                 "• M.Sc. (Computer Science) and M.Com."},
    {"intent": "admission",
     "keywords": ["admission", "admissions", "apply", "application", "enroll", "enrol",
                  "join", "registration", "register", "eligibility", "eligible"],
     "response": "Admissions are merit-based.\n"
                 "• Eligibility (UG): 12th pass with minimum 60%\n"
                 "• Apply online on the college website or at the admission office\n"
                 "• Application window: May to July every year."},
    {"intent": "documents",
     "keywords": ["document", "documents", "certificate", "certificates", "marksheet",
                  "required", "papers", "bring"],
     "response": "Documents required:\n1. 10th and 12th marksheets (original + 2 copies)\n"
                 "2. School Leaving Certificate\n3. Aadhaar card copy\n"
                 "4. 4 passport-size photos\n5. Caste / income certificate (if applicable)"},
    {"intent": "fees",
     "keywords": ["fee", "fees", "cost", "tuition", "payment", "pay", "charges", "price",
                  "how much"],
     "response": "Approximate annual fees:\n • B.Tech: ₹1,25,000\n• B.Sc.: ₹1,00,000\n• B.Com.: ₹1,00,000\n"
                 "• BCA: ₹1,25,000\n• BA: ₹1,00,000\n• PG programs: ₹1,20,000–₹1,30,000\n"
                 "Pay online or at the accounts office in two installments."},
    {"intent": "scholarship",
     "keywords": ["scholarship", "scholarships", "financial aid", "concession", "waiver"],
     "response": "Scholarships:\n• Government scholarships for SC/ST/OBC/EWS\n"
                 "• Merit scholarship for 85%+in 12th\n• Sports quota fee concession\n"
                 "Apply at the scholarship cell with income and caste certificates."},
    {"intent": "hostel",
     "keywords": ["hostel", "accommodation", "stay", "room", "mess", "boarding"],
     "response": "Separate boys' and girls' hostels with Wi-Fi, mess, 24x7 security and a "
                 "study room. Fee: ₹45,000/year including food. Apply at the hostel office "
                 "after admission is confirmed."},
    {"intent": "library",
     "keywords": ["library", "book", "books", "reading", "journal", "borrow"],
     "response": "Central library: 25,000+ books, journals and an e-library.\n"
                 "Timings: 9:00 AM – 6:00 PM (Mon–Sat). Borrow 3 books for 14 days."},
    {"intent": "placement",
     "keywords": ["placement", "placements", "job", "jobs", "recruit", "company",
                  "companies", "package", "salary", "internship", "career"],
     "response": "The Training & Placement Cell runs aptitude training, mock interviews and "
                 "campus drives. Last year: 70% placed, average ₹4 LPA, highest ₹8 LPA."},
    {"intent": "timings",
     "keywords": ["time", "timing", "timings", "hours", "schedule", "open", "close", "working"],
     "response": "College: 8:00 AM – 2:00 PM (Mon–Sat)\nOffice: 10:00 AM – 4:00 PM\nSunday closed & public holidays off."},
    {"intent": "contact",
     "keywords": ["contact", "phone", "call", "email", "mail", "address", "location",
                  "where", "reach", "website"],
     "response": f"{COLLEGE_NAME}\n📍BVM Mech Workshop,Shashtri Maidan Walkway,Mota Bazaar,Vallabh Vidhyanagar,Anand,Gujrat – 388120\n"
                 "📞 02692 238 001 \n✉ adminoffice@cvm.edu.in \n🌐 www.cvmu.edu.in"},
    {"intent": "facilities",
     "keywords": ["facility", "facilities", "lab", "labs", "canteen", "sports", "ground",
                  "wifi", "wi-fi", "campus", "bus", "transport", "gym"],
     "response": "Facilities: computer & science labs, canteen, sports ground, gym, Wi-Fi "
                 "campus and college bus service on major routes."},
    {"intent": "exam",
     "keywords": ["exam", "exams", "examination", "result", "results", "marks",
                  "syllabus", "semester", "internal"],
     "response": "We follow the semester system. Internals are held mid-semester and "
                 "university exams at the end. Results and syllabus are on the notice "
                 "board and website."},
    {"intent": "events",
     "keywords": ["event", "events", "fest", "festival", "club", "clubs", "cultural events",
                  "ncc", "nss", "activities"],
     "response": "Student life: annual cultural fest, tech symposium, NCC, NSS, coding club, "
                 "literary club and a yearly sports meet."},
    {"intent": "thanks",
     "keywords": ["thanks", "thank", "thank you", "thx", "great", "helpful"],
     "response": "You're welcome! Ask me anything else about the college."},
    {"intent": "bye",
     "keywords": ["bye", "goodbye", "see you", "exit", "quit"],
     "response": "Goodbye! Best of luck with your admission. 😊"},
]

FALLBACK = ("Sorry, I couldn't understand that. Try asking about admission, courses, "
            "fees, scholarship, hostel, library, placement, timings, facilities or contact.")

QUICK_BUTTONS = ["Admission", "Courses", "Fees", "Hostel", "Placement", "Contact"]

# =====================================================================
# 2. AI ENGINE  (pre-processing + keyword scoring + rule selection)
# =====================================================================
STOP_WORDS = {"the", "is", "are", "a", "an", "of", "for", "to", "in", "on", "me", "please",
              "tell", "about", "can", "you", "i", "my", "do", "does", "what", "want",
              "know", "give", "there"}


def preprocess(text):
    """Lower-case and remove punctuation."""
    return re.sub(r"[^a-z0-9\s\-]", " ", text.lower().strip())


def tokenize(text):
    """Split into words and drop stop-words."""
    return [t for t in preprocess(text).split() if t not in STOP_WORDS]


def score_rule(clean_text, tokens, keywords):
    """Word match = +1, phrase match = +2, simple stemming for longer words."""
    score, padded = 0, f" {clean_text} "
    for kw in keywords:
        if " " in kw:
            if f" {kw} " in padded:
                score += 2
        elif kw in tokens:
            score += 1
        elif len(kw) > 4 and any(t.startswith(kw[:-1]) for t in tokens):
            score += 1
    return score


def get_response(user_input):
    """Return (intent, reply) for the rule with the highest score."""
    clean, tokens = preprocess(user_input), tokenize(user_input)
    best_rule, best_score = None, 0
    for rule in RULES:
        s = score_rule(clean, tokens, rule["keywords"])
        if s > best_score:
            best_rule, best_score = rule, s
    if best_rule is None:
        return "fallback", FALLBACK
    return best_rule["intent"], best_rule["response"]


# =====================================================================
# 3. GUI  (Tkinter) - light/dark theme, chat bubbles, quick chips
# =====================================================================
THEMES = {
    "light": {"bg": "#f4f6fb", "header": "#1f3a8a", "header_sub": "#bfdbfe",
              "user_bg": "#2563eb", "user_fg": "#ffffff",
              "bot_bg": "#ffffff", "bot_fg": "#111827",
              "muted": "#6b7280", "chip": "#e0e7ff", "chip_fg": "#1f3a8a",
              "chip_hover": "#c7d2fe", "input_bg": "#ffffff", "input_fg": "#111827",
              "send": "#1f3a8a", "send_hover": "#2d4fb8"},
    "dark":  {"bg": "#111827", "header": "#0b1220", "header_sub": "#93c5fd",
              "user_bg": "#3b82f6", "user_fg": "#ffffff",
              "bot_bg": "#1f2937", "bot_fg": "#f3f4f6",
              "muted": "#9ca3af", "chip": "#1e293b", "chip_fg": "#93c5fd",
              "chip_hover": "#334155", "input_bg": "#1f2937", "input_fg": "#f3f4f6",
              "send": "#3b82f6", "send_hover": "#2563eb"},
}
PLACEHOLDER = "Type your question here..."
FONT = "Segoe UI"


class ChatbotApp:
    def __init__(self, root):
        self.root = root
        self.mode = "light"
        self.placeholder_on = False
        root.title("College Enquiry Chatbot")
        root.geometry("480x680")
        root.minsize(400, 520)

        # ---------- header
        self.header = tk.Frame(root)
        self.header.pack(fill="x")
        self.avatar = tk.Label(self.header, text="🎓", font=(FONT, 20), width=2)
        self.avatar.pack(side="left", padx=(12, 4), pady=10)
        info = tk.Frame(self.header)
        info.pack(side="left", pady=8)
        self.title_lbl = tk.Label(info, text=COLLEGE_NAME, font=(FONT, 12, "bold"), anchor="w")
        self.title_lbl.pack(anchor="w")
        self.status_lbl = tk.Label(info, text="● Online – Enquiry Assistant", font=(FONT, 9), anchor="w")
        self.status_lbl.pack(anchor="w")
        self.theme_btn = tk.Button(self.header, text="🌙", relief="flat", bd=0, font=(FONT, 13),
                                   cursor="hand2", command=self.toggle_theme)
        self.theme_btn.pack(side="right", padx=12)

        # ---------- chat area
        self.chat = scrolledtext.ScrolledText(root, wrap="word", state="disabled", bd=0,
                                              padx=12, pady=10, font=(FONT, 10),
                                              highlightthickness=0, cursor="arrow")
        self.chat.pack(fill="both", expand=True)

        # ---------- typing indicator
        self.typing_lbl = tk.Label(root, text="", font=(FONT, 9, "italic"), anchor="w")
        self.typing_lbl.pack(fill="x", padx=14)

        # ---------- quick-reply chips
        self.chip_frame = tk.Frame(root)
        self.chip_frame.pack(fill="x", padx=8, pady=(2, 4))
        self.chips = []
        for i, label in enumerate(QUICK_BUTTONS):
            b = tk.Button(self.chip_frame, text=label, relief="flat", bd=0, cursor="hand2",
                          font=(FONT, 9, "bold"), pady=4,
                          command=lambda l=label: self.send(l))
            b.grid(row=0, column=i, padx=2, sticky="ew")
            self.chip_frame.columnconfigure(i, weight=1)
            self.chips.append(b)

        # ---------- input row
        self.bottom = tk.Frame(root)
        self.bottom.pack(fill="x", padx=8, pady=(0, 10))
        self.entry = tk.Entry(self.bottom, font=(FONT, 11), relief="flat", bd=0,
                              highlightthickness=1)
        self.entry.pack(side="left", fill="x", expand=True, ipady=8, padx=(0, 6))
        self.entry.bind("<Return>", lambda e: self.send())
        self.entry.bind("<FocusIn>", self._focus_in)
        self.entry.bind("<FocusOut>", self._focus_out)
        self.send_btn = tk.Button(self.bottom, text="Send ➤", relief="flat", bd=0,
                                  font=(FONT, 10, "bold"), padx=14, cursor="hand2",
                                  command=self.send)
        self.send_btn.pack(side="left", ipady=6)
        self.clear_btn = tk.Button(self.bottom, text="🗑", relief="flat", bd=0,
                                   font=(FONT, 11), cursor="hand2", command=self.clear)
        self.clear_btn.pack(side="left", padx=(4, 0), ipady=4)

        self._hover(self.send_btn, "send", "send_hover")
        for c in self.chips:
            self._hover(c, "chip", "chip_hover")

        self.apply_theme()
        self._show_placeholder()
        self.add_message("bot", get_response("hello")[1])

    # ------------------------------------------------------------ theme
    def apply_theme(self):
        t = THEMES[self.mode]
        self.root.configure(bg=t["bg"])
        for w in (self.header, self.avatar, self.title_lbl, self.status_lbl, self.theme_btn):
            w.configure(bg=t["header"])
        self.avatar.master.configure(bg=t["header"])
        self.title_lbl.master.configure(bg=t["header"])
        self.title_lbl.configure(fg="white")
        self.status_lbl.configure(fg=t["header_sub"])
        self.theme_btn.configure(fg="white", activebackground=t["header"],
                                 text="☀" if self.mode == "dark" else "🌙")
        self.chat.configure(bg=t["bg"])
        self.chat.tag_configure("user", background=t["user_bg"], foreground=t["user_fg"],
                                justify="right", lmargin1=90, lmargin2=90, rmargin=8,
                                spacing1=8, spacing3=8)
        self.chat.tag_configure("bot", background=t["bot_bg"], foreground=t["bot_fg"],
                                justify="left", lmargin1=8, lmargin2=8, rmargin=90,
                                spacing1=8, spacing3=8)
        self.chat.tag_configure("time_user", foreground=t["muted"], font=(FONT, 8), justify="right",
                                rmargin=8, lmargin1=90)
        self.chat.tag_configure("time_bot", foreground=t["muted"], font=(FONT, 8), justify="left",
                                lmargin1=8)
        self.typing_lbl.configure(bg=t["bg"], fg=t["muted"])
        self.chip_frame.configure(bg=t["bg"])
        for c in self.chips:
            c.configure(bg=t["chip"], fg=t["chip_fg"], activebackground=t["chip_hover"],
                        activeforeground=t["chip_fg"])
        self.bottom.configure(bg=t["bg"])
        self.entry.configure(bg=t["input_bg"], insertbackground=t["input_fg"],
                             highlightbackground=t["muted"], highlightcolor=t["send"])
        self.send_btn.configure(bg=t["send"], fg="white", activebackground=t["send_hover"],
                                activeforeground="white")
        self.clear_btn.configure(bg=t["bg"], fg=t["muted"], activebackground=t["bg"])
        self._refresh_entry_color()

    def toggle_theme(self):
        self.mode = "dark" if self.mode == "light" else "light"
        self.apply_theme()

    def _hover(self, widget, normal, hover):
        widget.bind("<Enter>", lambda e: widget.configure(bg=THEMES[self.mode][hover]))
        widget.bind("<Leave>", lambda e: widget.configure(bg=THEMES[self.mode][normal]))

    # ------------------------------------------------------------ placeholder
    def _show_placeholder(self):
        self.entry.delete(0, "end")
        self.entry.insert(0, PLACEHOLDER)
        self.placeholder_on = True
        self._refresh_entry_color()

    def _refresh_entry_color(self):
        t = THEMES[self.mode]
        self.entry.configure(fg=t["muted"] if self.placeholder_on else t["input_fg"])

    def _focus_in(self, _):
        if self.placeholder_on:
            self.entry.delete(0, "end")
            self.placeholder_on = False
            self._refresh_entry_color()

    def _focus_out(self, _):
        if not self.entry.get().strip():
            self._show_placeholder()

    # ------------------------------------------------------------ chat logic
    def add_message(self, sender, text):
        stamp = datetime.now().strftime("%I:%M %p")
        self.chat.configure(state="normal")
        self.chat.insert("end", f"  {text}  \n", sender)
        who = "You" if sender == "user" else "Bot"
        self.chat.insert("end", f"{who} • {stamp}\n", f"time_{sender}")
        self.chat.configure(state="disabled")
        self.chat.see("end")

    def send(self, text=None):
        if text is None:
            if self.placeholder_on:
                return
            text = self.entry.get()
        text = text.strip()
        if not text:
            return
        self.entry.delete(0, "end")
        self.add_message("user", text)
        intent, reply = get_response(text)

        self.typing_lbl.configure(text="Bot is typing…")
        self.root.after(600, lambda: self._bot_reply(reply))
        if intent == "bye":
            self.root.after(2500, self.root.destroy)

    def _bot_reply(self, reply):
        self.typing_lbl.configure(text="")
        self.add_message("bot", reply)

    def clear(self):
        self.chat.configure(state="normal")
        self.chat.delete("1.0", "end")
        self.chat.configure(state="disabled")
        self.add_message("bot", get_response("hello")[1])


if __name__ == "__main__":
    root = tk.Tk()
    ChatbotApp(root)
    root.mainloop()