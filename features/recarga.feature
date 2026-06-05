Feature: Cálculo de recargas de celular
  Como operador de RecargaYa S.A.S.
  Quiero calcular correctamente el valor y la bonificación de cada recarga
  Para garantizar que los usuarios reciban los datos correctos

  Scenario: Recarga rechazada por monto inferior al mínimo
    Given que el usuario intenta recargar $999 pesos
    And el usuario no tiene plan premium
    When se procesa la recarga
    Then la recarga es rechazada
    And el mensaje indica que el monto está fuera del rango permitido

  Scenario: Recarga rechazada por monto superior al máximo
    Given que el usuario intenta recargar $50001 pesos
    And el usuario no tiene plan premium
    When se procesa la recarga
    Then la recarga es rechazada
    And el mensaje indica que el monto está fuera del rango permitido

  Scenario: Recarga mínima aceptada sin bonificación
    Given que el usuario intenta recargar $1000 pesos
    And el usuario no tiene plan premium
    When se procesa la recarga
    Then la recarga es aceptada
    And la bonificación de datos es del 0%

  Scenario: Usuario premium recibe bonificación adicional en recarga alta
    Given que el usuario intenta recargar $30000 pesos
    And el usuario tiene plan premium
    When se procesa la recarga
    Then la recarga es aceptada
    And la bonificación de datos es del 30%

  Scenario Outline: Bonificación según rango de monto para usuario estándar
    Given que el usuario intenta recargar <monto> pesos
    And el usuario no tiene plan premium
    When se procesa la recarga
    Then la recarga es <estado>
    And la bonificación de datos es del <bonificacion>%

    Examples:
      | monto | estado    | bonificacion |
      | 500   | rechazada | 0            |
      | 5000  | aceptada  | 0            |
      | 10000 | aceptada  | 10           |
      | 29999 | aceptada  | 10           |
      | 30000 | aceptada  | 25           |
      | 50000 | aceptada  | 25           |
      | 60000 | rechazada | 0            |