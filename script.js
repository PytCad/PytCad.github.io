// Funkcja do wyświetlania szczegółów na podstawie przekazanego parametru
function showDetails(type) {
    const details = {
        engine: "Silniki graficzne pozwalają na renderowanie 2D i 3D. Biblioteki takie jak Pygame są idealne dla gier.",
        cad: "Modelowanie CAD w Pythonie jest możliwe dzięki bibliotekom jak FreeCAD czy OCC. Twórz precyzyjne modele 3D."
    };

    alert(details[type] || "Brak dostępnych szczegółów.");
}

// Dodatkowa interakcja - zmiana koloru przycisków po kliknięciu
document.querySelectorAll('button').forEach(button => {
    button.addEventListener('click', () => {
        button.style.backgroundColor = '#ff5722';
        setTimeout(() => {
            button.style.backgroundColor = '#6a11cb';
        }, 500);
    });
});
