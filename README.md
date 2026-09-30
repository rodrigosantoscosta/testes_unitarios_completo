# testes_unitarios_completo
Todas as etapas da aula de testes unitários com IA.

---

## 📍 Branch `main` — Fundamentos (Fase 1)

Esta branch é a **linha de desenvolvimento dos fundamentos**. Ela contém o
ponto de partida da aula: uma única função, os cenários pensados de forma
intuitiva e os testes na forma mais básica do Pytest. É mantida separada das
demais branches (`desafio_final`, `chore/prune-tests`) de propósito — cada uma
documenta uma fase do aprendizado, sem merge entre elas.

### O que foi feito

| Arquivo | Papel |
|---|---|
| `src/tech/angelofdiasg/qabank/operacoes/validador_conta.py` | Função sob teste: `validar_abertura_conta(idade, score_credito)` |
| `src/tests/cenários/cenarios_iniciais.txt` | Cenários escritos **antes** do código de teste (análise) |
| `src/tests/test_validador.py` | 4 testes, um por cenário, com repetição de código |
| `pytest.ini` | Configuração: `pythonpath = src` e `testpaths = src/tests` |

### Regra de negócio praticada

`validar_abertura_conta(idade, score_credito)`:

1. `idade < 18` → lança `ValueError("Menor de idade não permitido")`
2. `score_credito <= 500` → retorna `"Recusado"`
3. caso contrário → retorna `"Aprovado"`

A ordem importa: a validação de idade acontece **antes** da checagem do score,
por isso um menor de idade com score alto ainda gera exceção (e não
`"Aprovado"`).

### Conceitos aplicados

**1. Teste de Caixa Preta — análise antes da automação**
O fluxo é sempre o mesmo: primeiro os **cenários** no `.txt`
(`cenarios_iniciais.txt`), depois o código de teste. O aluno pensa em
*entradas* e *resultados esperados* sem olhar a implementação — só o contrato.

**2. Caminho Feliz (Happy Path)**
Cenário 1 (idade 25, score 800 → `Aprovado`) exercita o único caminho em que
nenhuma regra rejeita. É a base: sem ele, nada está funcionando de verdade.

**3. Partições de Equivalência (rascunho intuitivo)**
Os 4 cenários cobrem as classes de entrada óbvias para um iniciante:
- idade válida + score alto → aprovado
- idade válida + score baixo → recusado
- idade inválida (com score alto) → exceção
- idade inválida + score baixo → exceção

É a versão "ingênua" da técnica: as partições estão certas, mas os **valores
de limite** (18 e 500 exatos) ainda não foram testados — isso é o próximo
passo do aprendizado (Análise de Valor Limite, nas branches seguintes).

**4. Tratamento de exceção com `pytest.raises`**
```python
with pytest.raises(ValueError, match="Menor de idade não permitido"):
    validar_abertura_conta(idade=15, score_credito=900)
```
`pytest.raises` valida **duas** coisas: que a exceção certa foi lançada e que
a mensagem (`match`, substring) corresponde ao contrato. Um teste que apenas
"espera qualquer erro" é fraco; a mensagem é parte do comportamento visível
ao chamador.

**5. Um teste por cenário (abordagem repetitiva)**
Cada cenário vira uma função `test_*` independente, com nome descritivo e
docstring explicando a intenção. É propositalmente verbosa: esta é a
**Fase 1**, feita para depois refatorar com `@pytest.mark.parametrize`
(Data-Driven Testing) e `@pytest.fixture` (Injeção de Dependência) nas
branches `feat/parametrize` e `feat/fixtures`.

**6. Estrutura de pastas e configuração**
- `pytest.ini` com `pythonpath = src` evita `sys.path` manual: os testes
  importam `from tech.angelofdiasg...` direto.
- `testpaths = src/tests` permite rodar simplesmente `python -m pytest`.
- Cada suíte em sua pasta (`src/tests/`), mantendo testes separados da
  produção (`src/tech/`).

### Como executar

Na raiz do projeto:

```
python -m pytest -v
```

### Mapa das branches (linhas de desenvolvimento separadas)

| Branch | Fase |
|---|---|
| **`main`** (esta) | Fundamentos: cenários intuitivos + Pytest básico + `pytest.raises` |
| `desafio_final` | Técnicas avançadas: Valor Limite/Partição, `parametrize`, fixtures |
| `chore/prune-tests` | Atividades de saque/transferência + auditoria com a skill `prune-tests` |

Bom estudo e bons testes! 🐛🔨
