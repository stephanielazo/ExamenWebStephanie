from flask import Flask, request, render_template, redirect, url_for, session, flash

app = Flask(__name__)

app.config['SECRET_KEY'] = 'MI_CLAVE_SECRETA'

USUARIOS = {
    "juan": "admin",
    "pepe": "user"
}
@app.route('/', methods=['GET', 'POST'])
def home():

    if request.method == 'POST':

        ejercicio = request.form.get('ejercicio')

        if ejercicio == '1':
            return redirect(url_for('ejercicio1'))
        elif ejercicio == '2':
            return redirect(url_for('ejercicio2'))


    return render_template('home.html')

@app.route('/ejercicio1', methods=['GET', 'POST'])
def ejercicio1():

    if request.method == 'POST':

        nombre = request.form.get('nombre')
        edad = request.form.get('edad')
        cantidad_tarros = request.form.get('cantidad_tarros')


        if not nombre or not edad or not cantidad_tarros:
            flash("Todos los campos son requeridos.", "error")
            return render_template('ejercicio1.html')

        try:

            edad = int(edad)
            cantidad_tarros = int(cantidad_tarros)
        except ValueError:
            flash("Edad y cantidad de tarros deben ser números válidos.", "error")
            return render_template('ejercicio1.html')

        precio_tarro = 9000

        total_sin_descuento = cantidad_tarros * precio_tarro


        if 18 <= edad <= 30:
            descuento = 0.15
        elif edad > 30:
            descuento = 0.25
        else:
            descuento = 0.0


        total_con_descuento = total_sin_descuento * (1 - descuento)


        descuento_en_dinero = total_sin_descuento - total_con_descuento


        return render_template('ejercicio1.html', nombre=nombre, edad=edad,
                               cantidad_tarros=cantidad_tarros, total_sin_descuento=total_sin_descuento,
                               total_con_descuento=total_con_descuento, descuento_en_dinero=descuento_en_dinero)


    return render_template('ejercicio1.html')

@app.route('/ejercicio2', methods=['GET', 'POST'])
def ejercicio2():

    if 'username' in session:
        return redirect(url_for('ejercicio2'))

    mensaje_bienvenida = None


    if request.method == 'POST':

        usuario = request.form.get('usuario')
        contrasena = request.form.get('contrasena')


        if usuario in USUARIOS and USUARIOS[usuario] == contrasena:

            session['username'] = usuario

            if usuario == 'juan':
                mensaje_bienvenida = f'Bienvenido administrador {usuario}'
            elif usuario == 'pepe':
                mensaje_bienvenida = f'Bienvenido usuario {usuario}'
        else:

            flash("Usuario o contraseña incorrectos.", "error")


    return render_template('ejercicio2.html', mensaje_bienvenida=mensaje_bienvenida)

@app.route('/logout')
def logout():

    session.pop('username', None)


    flash("Has cerrado sesión correctamente.", "success")

    return redirect(url_for('ejercicio2'))

if __name__ == '__main__':
    app.run(debug=True)
