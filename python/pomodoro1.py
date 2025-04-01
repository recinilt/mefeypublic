import time
import winsound

def play_alarm():
    winsound.PlaySound("alarm.wav", winsound.SND_FILENAME)

def get_user_input(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value > 0:
                return value
            else:
                print("Lütfen pozitif bir sayı girin.")
        except ValueError:
            print("Geçerli bir sayı girin.")

def countdown(duration, label_text):
    for t in range(duration, -1, -1):
        mins, secs = divmod(t, 60)
        print(f"{label_text}: {mins:02}:{secs:02}", end="\r")
        time.sleep(1)

def start_timer(work_duration, short_break, long_break, cycles, repeats):
    for repeat in range(repeats):  # Repeat the entire sequence 'repeats' times
        print(f"\n---- {repeat + 1}. Tekrar Başlıyor ----")
        for cycle in range(cycles):
            print(f"\nDöngü {cycle + 1}/{cycles}")
            countdown(work_duration, "Spor Süresi")
            play_alarm()
            if cycle < cycles - 1:  # Short break between work periods
                countdown(short_break, "Kısa Ara")
                play_alarm()
        countdown(long_break, "Uzun Ara")  # Long break after all cycles
        play_alarm()
    print("\nPomodoro Tamamlandı!")

# Get user input for durations
print("Pomodoro Zaman Yönetimi Aracı\n")
work_duration = get_user_input("Spor süresini dakika cinsinden girin: ") * 60
short_break = get_user_input("Kısa ara süresini dakika cinsinden girin: ") * 60
long_break = get_user_input("Uzun ara süresini dakika cinsinden girin: ") * 60
cycles = get_user_input("Her tekrar için kaç döngü olsun?: ")
repeats = get_user_input("Kaç tekrar yapmak istiyorsunuz?: ")

# Start timer
start_timer(work_duration, short_break, long_break, cycles, repeats)
