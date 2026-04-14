import pandas as pd
import numpy as np

# ── 1. LOAD THE DATA ──────────────────────────────────────────
df = pd.read_csv("messy_data.csv")

print("=" * 50)
print("RAW DATA — before cleaning")
print("=" * 50)
print(df)
print()


# ── 2. INSPECT THE DATA ───────────────────────────────────────
print("Shape:", df.shape)           # rows x columns
print()
print("Data types:")
print(df.dtypes)
print()
print("Missing values per column:")
print(df.isnull().sum())
print()


# ── 3. FIX NULL / MISSING VALUES ─────────────────────────────

# Replace the word "NULL" (string) with actual NaN first
df.replace("NULL", np.nan, inplace=True)

# Fill missing names with "Unknown"
df["name"].fillna("Unknown", inplace=True)

# Fill missing salary with the average salary
avg_salary = pd.to_numeric(df["salary"], errors="coerce").mean()
df["salary"] = pd.to_numeric(df["salary"], errors="coerce")
df["salary"].fillna(avg_salary, inplace=True)

# Fill missing joining_date with a default
df["joining_date"].fillna("2000-01-01", inplace=True)

print("After fixing NULLs:")
print(df.isnull().sum())
print()


# ── 4. FIX DATA TYPES ────────────────────────────────────────

# Age column has "abc" in it — force convert, bad values become NaN
df["age"] = pd.to_numeric(df["age"], errors="coerce")

# Fill bad age values with median age
median_age = df["age"].median()
df["age"].fillna(median_age, inplace=True)

# Convert age to integer
df["age"] = df["age"].astype(int)

# Convert salary to integer
df["salary"] = df["salary"].astype(int)

# Convert joining_date to proper date format
df["joining_date"] = pd.to_datetime(df["joining_date"])

print("Data types after fixing:")
print(df.dtypes)
print()


# ── 5. FIX INCONSISTENT TEXT ─────────────────────────────────

# Department names are inconsistent: "it", "IT", "hr", "HR"
df["department"] = df["department"].str.upper().str.strip()

print("Unique departments after fixing:")
print(df["department"].unique())
print()


# ── 6. REMOVE DUPLICATES ─────────────────────────────────────
before = len(df)
df.drop_duplicates(inplace=True)
after = len(df)
print(f"Removed {before - after} duplicate rows")
print()


# ── 7. EXPLORE THE CLEAN DATA ────────────────────────────────
print("=" * 50)
print("CLEAN DATA — after fixing")
print("=" * 50)
print(df)
print()

print("Summary statistics:")
print(df.describe())
print()

print("Average salary by department:")
print(df.groupby("department")["salary"].mean().round(0))
print()

print("Employee count by department:")
print(df["department"].value_counts())
print()


# ── 8. SAVE THE CLEAN DATA ───────────────────────────────────
df.to_csv("clean_data.csv", index=False)
print("Clean data saved to clean_data.csv ✅")