city: "Berlin"
target_districts:
  - "Prenzlauer Berg"
  - "Friedrichshain"
  - "Mitte"
preferred_states:
  - "Berlin"
  - "Berlin-Mitte"
property_types:
  - "apartment"
  - "house"
max_price: 2200
min_size_m2: 55
max_radius_km: 8
preferred_beds: 2
top_n: 3
email_to: ""
email_from: ""
smtp_host: ""
smtp_port: 587
smtp_user: ""
smtp_password: ""

# Set these in GitHub Actions secrets for the scheduled run.
# Example:
# email_to: "you@example.com"
# email_from: "you@example.com"
# smtp_host: "smtp.example.com"
# smtp_user: "your-user"
# smtp_password: "your-password"
