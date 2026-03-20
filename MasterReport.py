from playwright.sync_api import sync_playwright
import os
import time
from datetime import datetime, timedelta
import calendar

MAX_REINTENTOS = 20


class AutomatizadorReportes:
    def __init__(self):
        self.url_reporte = os.environ.get("REPORT_URL", "")
        if not self.url_reporte:
            raise ValueError("Define la variable de entorno REPORT_URL con la URL del sistema de reportes")
        self.contador_vueltas = 0

    def calcular_fechas(self, meses_atras):
        hoy = datetime.now()

        año = hoy.year
        mes = hoy.month - meses_atras

        while mes <= 0:
            mes += 12
            año -= 1

        primer_dia = datetime(año, mes, 1)
        ultimo_dia_num = calendar.monthrange(año, mes)[1]
        ultimo_dia = datetime(año, mes, ultimo_dia_num)

        fecha_inicio = primer_dia.strftime("%d/%m/%Y")
        fecha_fin = ultimo_dia.strftime("%d/%m/%Y")
        nombre_mes = primer_dia.strftime("%B").capitalize()

        return fecha_inicio, fecha_fin, f"{nombre_mes} {año}"

    def seleccionar_fecha(self, page, indice, fecha):
        try:
            campos = page.locator("input[data-role='datepicker']").all()

            if len(campos) > indice:
                campo = campos[indice]
                campo.fill("")
                campo.fill(fecha)
                return True
            return False
        except Exception:
            return False

    def intentar_click_preview(self, page):
        try:
            boton = page.locator("button[aria-label='Preview the report'], .trv-parameters-area-preview-button").first

            if boton.count() == 0:
                return False, "No existe"

            if not boton.is_visible():
                return False, "No visible"

            if boton.get_attribute("disabled") is not None:
                return False, "Deshabilitado"

            boton.click(timeout=5000)
            return True, "Click exitoso"

        except Exception as e:
            return False, str(e)[:50]

    def ejecutar_consulta_con_reintentos(self, page, meses):
        fecha_inicio, fecha_fin, desc = self.calcular_fechas(meses)

        print(f"\n   {desc}: {fecha_inicio} - {fecha_fin}")
        print(f"   {'='*50}")

        intento = 0
        inicio_consulta = time.time()

        while intento < MAX_REINTENTOS:
            intento += 1
            tiempo_transcurrido = int(time.time() - inicio_consulta)

            print(f"\n      Intento #{intento}/{MAX_REINTENTOS} (tiempo: {tiempo_transcurrido}s)")
            print(f"         Seleccionando fechas...")
            self.seleccionar_fecha(page, 0, fecha_inicio)
            self.seleccionar_fecha(page, 1, fecha_fin)
            time.sleep(1)

            print(f"         Intentando click en Preview...")
            exito, razon = self.intentar_click_preview(page)

            if exito:
                print(f"         Click exitoso en intento #{intento} ({tiempo_transcurrido}s)")
                time.sleep(5)
                return True
            else:
                print(f"         Click falló: {razon}. Reintentando en 30s...")
                time.sleep(30)

        print(f"   Se alcanzó el máximo de {MAX_REINTENTOS} reintentos sin éxito")
        return False

    def bucle_infinito(self, page):
        print("\n" + "="*70)
        print("Iniciando bucle - 30 minutos entre vueltas")
        print("Ctrl+C para detener")
        print("="*70)

        vuelta = 0
        while True:
            vuelta += 1
            self.contador_vueltas = vuelta
            print(f"\n{'='*70}")
            print(f"Vuelta #{vuelta} - {datetime.now().strftime('%H:%M:%S')}")
            print(f"{'='*70}")

            exitos = 0
            for meses in [1, 2, 3]:
                if self.ejecutar_consulta_con_reintentos(page, meses):
                    exitos += 1
                time.sleep(3)

            print(f"\n   Vuelta #{vuelta}: {exitos}/3 consultas exitosas")

            proxima = datetime.now() + timedelta(minutes=30)
            print(f"\n   Esperando 30 minutos. Próxima vuelta: {proxima.strftime('%H:%M:%S')}")
            time.sleep(1800)

    def ejecutar(self):
        print("="*70)
        print("Automatizador de Reportes")
        print("="*70)

        with sync_playwright() as p:
            print("Iniciando Microsoft Edge...")
            browser = p.chromium.launch(
                headless=False,
                channel="msedge",
                args=['--start-maximized']
            )

            context = browser.new_context()
            page = context.new_page()

            print(f"Navegando a: {self.url_reporte}")
            page.goto(self.url_reporte, timeout=60000)

            print("\n" + "="*70)
            print("Inicia sesión con tu cuenta corporativa")
            print("Cuando el reporte esté cargado, presiona ENTER")
            print("="*70)

            # Pausa intencional para login SSO manual
            input("\nPresiona ENTER cuando estés listo...")

            controles = page.locator("button[aria-label='select']").count()
            if controles >= 2:
                print("Página de reportes confirmada")
                time.sleep(3)

                try:
                    self.bucle_infinito(page)
                except KeyboardInterrupt:
                    print("\nPrograma detenido")
            else:
                print(f"No se encontraron los controles del reporte (se encontraron {controles} de 2 esperados)")
                input("\nPresiona ENTER para cerrar...")

            context.close()
            browser.close()


if __name__ == "__main__":
    try:
        auto = AutomatizadorReportes()
        auto.ejecutar()
    except KeyboardInterrupt:
        print("\nPrograma detenido")
    except Exception as e:
        print(f"Error: {e}")
