from pathlib import Path

p = Path("accounts/templates/accounts/home.html")
content = p.read_text(encoding="utf-8")

old = """<a href="{% url 'register' %}" class="btn-register">Register</a>"""

new = old + """
<li class="nav-item ms-lg-2 mt-3 mt-lg-0">
    <a href="/admin/" class="btn-register">Admin Login</a>
</li>"""

if content.count(old) != 1:
    print("ERROR: Register button was not found exactly once. No changes made.")
else:
    p.write_text(content.replace(old, new), encoding="utf-8")
    print("Admin Login button added successfully!")
