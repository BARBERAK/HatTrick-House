# features/apuestas.feature
Feature: Gestión de Apuestas
  Como usuario registrado
  Quiero poder crear, editar y eliminar mis apuestas
  Para gestionar mi dinero en HatTrick House

  Background:
    Given Existe un usuario "testuser" con contraseña "password123" y saldo "100"
    And El usuario inicia sesión con "testuser" y "password123"
    And Existe un partido "Real Madrid" vs "Barcelona" con id "game1"

  Scenario: Crear una apuesta correctamente
    When El usuario visita la página del partido "game1"
    And Selecciona la opción "1" con cuota "2.50"
    And Introduce la cantidad "20"
    And Hace clic en "REALIZAR APUESTA"
    Then Se muestra un mensaje de éxito
    And La apuesta aparece en su lista de "Mis Apuestas"
    And El saldo del usuario es "80"

  Scenario: Error al editar una apuesta sin saldo suficiente
    Given El usuario tiene una apuesta de "20" euros en el partido "game1"
    When El usuario edita la apuesta al nuevo valor de "200" euros
    Then Se muestra un mensaje de error diciendo "No tienes saldo suficiente"
    And La apuesta original de "20" euros se mantiene

  Scenario: Eliminar una apuesta correctamente
    Given El usuario tiene una apuesta de "20" euros en el partido "game1"
    When El usuario visita la página de sus apuestas
    And El usuario hace clic en "ELIMINAR APUESTA"
    Then Se muestra un mensaje de éxito
    And La apuesta desaparece de "Mis Apuestas"
    And El saldo del usuario vuelve a ser "100"