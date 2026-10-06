# Bootcamp QA: Fundamentos de Testes com Pytest

Este repositório pratica testes de caixa preta com o framework Pytest em Python.
As técnicas principais são Análise de Valor Limite e Partição de Equivalência.
O projeto mostra como a escrita de testes evolui ao longo do curso.

## Objetivo

O objetivo não é apenas escrever testes. O objetivo é evoluir na escrita deles.
O curso começa com uma abordagem simples e repetitiva.
Depois, aplica duas técnicas profissionais:

- Data-Driven Testing com `@pytest.mark.parametrize`.
- Injeção de Dependência com `@pytest.fixture`.

## Estrutura do repositório

- `src/tech/` guarda o código de produção.
- `src/tests/` guarda os testes automatizados.
- `src/tests/cenários/` guarda os documentos de análise.
- `pytest.ini` define `pythonpath = src` e `testpaths = src/tests`.

## Roteiro de branches

O repositório tem três branches. Cada branch guarda uma fase do curso.

| Branch | Conteúdo |
|---|---|
| `main` | Fundamentos: função inicial, cenários intuitivos e testes básicos. |
| `desafio_final` | Valor Limite, Partição de Equivalência, `parametrize` e fixtures. |
| `chore/prune-tests` | Atividades de saque e transferência, e auditoria `prune-tests`. |

Use `git checkout <nome-da-branch>` para trocar de branch.

## Fase 1: Fundamentos

### O que foi feito

| Arquivo | Papel |
|---|---|
| `src/tech/angelofdiasg/qabank/operacoes/validador_conta.py` | Função `validar_abertura_conta(idade, score_credito)`. |
| `src/tests/cenários/cenarios_iniciais.txt` | Cenários pensados antes do código de teste. |
| `src/tests/tests_validador_conta/test_validador.py` | Quatro testes, um por cenário. |
| `pytest.ini` | Configuração do Pytest. |

### Regra de negócio

`validar_abertura_conta(idade, score_credito)` aplica três regras:

1. Se `idade < 18`, lança `ValueError("Menor de idade não permitido")`.
2. Se `score_credito <= 500`, retorna `"Recusado"`.
3. Nos outros casos, retorna `"Aprovado"`.

A validação de idade roda antes da checagem do score.
Por isso, um menor de idade com score alto ainda gera erro.

### Conceitos aplicados

**Caixa preta.** Escreva os cenários antes dos testes. Cada cenário define entrada e resultado esperado, sem consultar a implementação.

**Caminho feliz.** O primeiro cenário exercita o caminho em que nenhuma regra rejeita a entrada.

**Partição de equivalência.** Os quatro cenários cobrem quatro classes de entrada. A primeira combina idade válida com score alto. A segunda combina idade válida com score baixo. A terceira combina idade inválida com score alto. A quarta combina idade inválida com score baixo.

Essa versão ainda não testa os limites exatos `18` e `500`. A Análise de Valor Limite cobre isso na fase seguinte.

**Exceção com `pytest.raises`.** O exemplo abaixo valida duas coisas: a classe da exceção e a mensagem.

```python
with pytest.raises(ValueError, match="Menor de idade não permitido"):
    validar_abertura_conta(idade=15, score_credito=900)
```

A mensagem faz parte do contrato. Um teste que aceita qualquer erro não detecta mudança de mensagem.

**Um teste por cenário.** Cada cenário vira uma função `test_*` separada. A repetição é proposital. É o ponto de partida que as próximas fases refatoram.

## Atividades guiadas

### Desconto (`calcular_desconto`)

A função aplica três faixas: até `100` sem desconto, de `101` a `500` com `10%` e acima de `500` com `20%`. Valores negativos geram `ValueError`.

Os oito cenários cobrem as quatro partições e as fronteiras `100/101` e `500/501`. Os testes existem em três formas, para comparação: direta, com `parametrize` e com fixtures.

### Saque (`validar_saque`)

A função valida um pedido de saque em quatro etapas, nesta ordem: tipo de conta, valor positivo, saldo e limite diário. O limite diário é `2000` para conta corrente e `1000` para conta poupança. A estrutura ausente gera `ValueError`.

A ordem das etapas importa. Ela define qual motivo de recusa aparece quando mais de uma regra falha.

### Transferência (`validar_transferencia`)

A função valida sete regras. Os limites são `1000` para conta corrente e `500` para conta poupança. Origem e destino precisam de números diferentes.

## Revisão com a skill `prune-tests`

A skill `prune-tests` audita testes frágeis ou tautológicos. Ela está salva em `~/.config/opencode/skills/prune-tests/SKILL.md` e está disponível em outras sessões.

### Audit e Cleanup

- **Audit**: pedidos como revisar ou analisar. É somente leitura. O resultado é um relatório.
- **Cleanup**: pedidos como podar ou reescrever. Autoriza as edições no escopo aprovado.

O escopo fica fixo. A decisão é tomada por teste, nunca por arquivo.

### A barra comportamental

Um teste só sobrevive se cumprir os seis itens abaixo:

1. Prova um comportamento exato vindo de um requisito aprovado.
2. Detecta uma falha visível ao usuário ou ao chamador.
3. Tem resultado esperado independente da implementação.
4. Observa pelo contrato público.
5. Sobrevive a refatores internos e a mudanças de texto ou layout.
6. Usa a menor camada de teste que dá confiança, sem duplicar cobertura.

Faltar um item leva ao conselho de remoção.

### O que podar

- **Tautologias**: o esperado é derivado do próprio cálculo de produção. O teste passa por construção.
- **Change detectors**: falham quando o código muda, sem apontar comportamento errado. Exemplos: leitura de fonte, contagem de elementos e snapshots de estrutura.
- **Geometria e aparência**: dimensões, estilos computados e contagem de linhas são evidência visual, não comportamento.
- **Texto**: asserção de frase exata só quando a palavra em si é requisito.
- **Foco e desabilitado**: mantenha só quando o estado é o contrato de interação.

### Disposições

| Disposição | Quando |
|---|---|
| `DELETE` | Viola a política e nenhum comportamento fica desprotegido. É o padrão. |
| `REWRITE` | O teste é inaceitável, mas contém comportamento que passa na barra. É exceção. |
| `KEEP` | Suspeito, mas prova comportamento aceitável e passa na barra sem mudar. |

`KEEP` e `REWRITE` exigem justificativa escrita para os seis itens da barra.

### Resultado nesta branch

Foram aplicados três `DELETE`, nenhum `REWRITE` e ficaram 32 casos `KEEP`. O código também perdeu um `import copy` sem uso.

- Uma duplicata do `ValueError` de saque.
- Um teste de isolamento de fixture que não exercitava a função pública.
- Um teste de imutabilidade sem requisito que o aprovasse.

## Como executar os testes

Na raiz do projeto:

```
python -m pytest -v
```

O `-v` mostra o nome de cada teste que passou ou falhou.

## Uso de IA na atividade

Durante a aula, explore como usar IA para gerar a estrutura dos arquivos Pytest.
O foco do QA é pensar nos cenários. A automação pode ser acelerada com prompts assertivos.
