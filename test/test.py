import os
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer
from cocotb_tools.runner import get_runner

# 1. Aquí va la lógica de tu testbench (lo que tenías en project_tb.py)
@cocotb.test()
async def tt_um_tt_screensaver_project(dut):
    """
    Testbench para verificar el proyecto VGA tt_um_tt_screensaver_project
    """
    # Reloj principal (periodo de 10 ns -> 100 MHz)
    clock = Clock(dut.clk, 10, unit="ns")
    cocotb.start_soon(clock.start())

    # Inicializar señales de control y entradas (Reset activo en bajo: rst_n)
    dut.rst_n.value = 0
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0

    await Timer(100, unit="ns")

    # Liberar el reset
    await RisingEdge(dut.clk)
    dut.rst_n.value = 1
    dut._log.info("Reset liberado. Iniciando simulación del proyecto VGA...")

    # Probar cambios en las entradas de configuración (ui_in)
    await Timer(50, unit="us")
    dut.ui_in.value = 2  # Activa modo amarillo
    dut._log.info("Cambiando a modo amarillo...")

    await Timer(50, unit="us")
    dut.ui_in.value = 1  # Activa modo tile
    dut._log.info("Cambiando a modo tile...")

    # Dejar correr la simulación para capturar ondas suficientes
    await Timer(100, unit="us")
    dut._log.info("Simulación finalizada exitosamente.")


# 2. Aquí va la configuración del runner que compila y ejecuta (lo que tenías en run_test.py)
def test_screensaver_runner():
    hdl_toplevel = "tt_um_tt_screensaver_project"
    
    # Rutas a tus fuentes Verilog (ajusta si están en ../src/)
    sources = [
        "project.v",
        "hvsync_generator.v",
        "bitmap_rom.v"
    ]

    runner = get_runner("icarus")
    runner.build(
        sources=sources,
        hdl_toplevel=hdl_toplevel,
        waves=True,
    )
    
    runner.test(
        hdl_toplevel=hdl_toplevel,
        test_module="test",  # Debe coincidir con el nombre de este archivo (test.py)
        waves=True,
        extra_env={"PYTHONPATH": os.path.abspath(".")},
    )

if __name__ == "__main__":
    test_screensaver_runner()
