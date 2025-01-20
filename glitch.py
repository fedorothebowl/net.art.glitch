from PIL import Image
import os
import random
import shutil

input_image_path = os.path.join(os.path.dirname(__file__), "input.png")
output_folder = os.path.join(os.path.dirname(__file__), "immagini_glitchate_200")

MAX_FOLDER_SIZE = 30 * 1024 * 1024 * 1024  # 30 GB in byte

# Funzione per calcolare la dimensione totale della cartella
def get_folder_size(folder):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size

# Carica l'immagine originale
img = Image.open(input_image_path).convert("RGBA")  # Converti in RGBA per la trasparenza

# Assicurati che la cartella di output esista
os.makedirs(output_folder, exist_ok=True)

# Ottieni larghezza, altezza e inizializza il totale dei pixel
width, height = img.size
pixels = img.load()

# Crea un set di tutte le coordinate dei pixel
all_coordinates = [(x, y) for x in range(width) for y in range(height)]
random.shuffle(all_coordinates)  # Mescola le coordinate per un ordine casuale

# Numero di pixel da eliminare per iterazione
pixels_to_remove_per_iteration = 200

# Inizializza il contatore dei cicli
cycles = 0

while all_coordinates:
    # Preleva 1000 pixel casuali dal set
    current_batch = all_coordinates[:pixels_to_remove_per_iteration]
    del all_coordinates[:pixels_to_remove_per_iteration]  # Rimuovi i pixel selezionati

    # Elimina i pixel (impostandoli trasparenti)
    for x, y in current_batch:
        pixels[x, y] = (0, 0, 0, 0)

    # Incrementa il contatore dei cicli
    cycles += 1

    # Salva un'immagine per ogni ciclo
    output_path = os.path.join(output_folder, f"glitch_{cycles}.png")
    img.save(output_path)

    # Controlla la dimensione della cartella
    folder_size = get_folder_size(output_folder)
    if folder_size > MAX_FOLDER_SIZE:
        print(f"Limite di 30 GB superato! La cartella ha raggiunto {folder_size / (1024 * 1024 * 1024):.2f} GB.")
        shutil.rmtree(output_folder)  # Rimuove la cartella di output
        print("Cartella di output eliminata.")
        break

    print(f"Ciclo {cycles}: immagine salvata in {output_path} - Pixel rimanenti: {len(all_coordinates)} - Cartella: {folder_size / (1024 * 1024 * 1024):.2f} GB")

# Salva l'immagine finale
if all_coordinates:
    final_output_path = os.path.join(output_folder, "immagine_finale.png")
    img.save(final_output_path)
    print(f"Immagine finale salvata in {final_output_path}")

# Stampa il numero totale di cicli
print(f"Processo completato in {cycles} cicli.")
