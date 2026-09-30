# 🧪 Bootcamp QA: Fundamentos de Testes com Pytest

Bem-vindos ao repositório prático do Bootcamp de Qualidade de Software!
Neste projeto, vão aprender e aplicar técnicas de testes de Caixa Preta (como Análise de Valor Limite) e automatizar a vossa estratégia utilizando o framework **Pytest** em Python.

---

## 🎯 Objetivo do Projeto
O objetivo não é apenas aprender a escrever testes, mas sim **como evoluir a escrita de testes**. 
Começaremos com uma abordagem mais simples (e repetitiva) e evoluiremos para técnicas profissionais de automação utilizando **Data-Driven Testing (Parametrize)** e **Injeção de Dependência (Fixtures)**.

---

## 🌳 Navegando pelas Branches (Roteiro de Aprendizagem)

Este repositório está dividido em **branches** (ramificações). Cada branch representa uma fase diferente do nosso aprendizado. Podem mudar de branch utilizando o comando `git checkout <nome-da-branch>` ou através da interface do GitHub.

### 1️⃣ Branch: `main` (O Início)
* **O que tem aqui:** A função inicial do desenvolvedor (`validador_conta.py`), os cenários de teste pensados de forma intuitiva, e a implementação de testes Pytest da forma mais básica (um teste para cada cenário, com repetição de código).
* **O que aprender:** A sintaxe básica do Pytest e o uso do `pytest.raises` para capturar exceções.

### 2️⃣ Branch: `feat/parametrize` (Subindo de Nível)
* **O que tem aqui:** Refatorámos os testes da branch `main` utilizando o poderoso decorador `@pytest.mark.parametrize`.
* **O que aprender:** Data-Driven Testing. Como uma única função de teste pode executar múltiplos cenários de uma Tabela de Decisão, tornando o código incrivelmente limpo e fácil de manter.

### 3️⃣ Branch: `feat/fixtures` (Injeção de Dados)
* **O que tem aqui:** Uma demonstração de como utilizar o `@pytest.fixture`.
* **O que aprender:** Como separar a "criação dos dados de teste" da "execução do teste". Entender como preparar ambientes (ou dados) e injetá-los automaticamente nos teus testes.

### 4️⃣ Branch: `feat/desafio-extra` (Modo Full-Stack)
* **O que tem aqui:** A resolução do desafio da funcionalidade `calcular_desconto`.
* **O que aprender:** Aplicação completa do que foi aprendido. Encontrarão a lógica de negócio implementada, os cenários baseados em Valor Limite/Partição de Equivalência, e os testes escritos das 3 formas diferentes (Direto, Parametrize e Fixtures) para efeitos de comparação.

---

## 🧩 Desafio Extra para a Aula

Nesta branch, o ficheiro `src/tests/cenários/cenarios_desafio_aluno.txt`
apresenta um novo exercício de validação de transferências bancárias. Ele
define o contrato, as regras e os cenários, mas não inclui implementação nem
testes de referência: a proposta é que vocês desenvolvam ambos, aplicando
`@pytest.mark.parametrize` e fixtures.

Os exemplos de desconto e de validação de cliente premium continuam disponíveis
como material de estudo; são independentes deste desafio.

## 🛠️ Atividade Completa: Implementar e Testar

A atividade de saque está organizada em etapas para vocês seguirem:

1. Ler os requisitos e critérios de aceite em
   `src/tech/angelofdiasg/qabank/operacoes/requisito_atividade_saque.txt`.
2. Implementar a função inicial em
   `src/tech/angelofdiasg/qabank/operacoes/validar_saque.py`.
3. Escrever os cenários manualmente em
   `src/tests/cenários/cenarios_atividade_saque.txt`.
4. Completar os testes em
   `src/tests/tests_validar_saque/test_validar_saque.py`, usando o
   `parametrize` e a fixture já preparados. Os testes-esqueleto estão ignorados
   até vocês removerem os marcadores de skip.

## 🚀 Como Executar os Testes

Para executar os testes em qualquer uma das branches, certifiquem-se de que estão na raiz do projeto e executem o seguinte comando no terminal:

`python -m pytest -v`

* **Dica:** O `-v` (verbose) permite ver exatamente qual o teste que passou ou falhou detalhadamente!

---

## 🤖 Uso da IA na Atividade
Durante a aula, exploraremos como utilizar a Inteligência Artificial (Copilot/ChatGPT/Gemini) para gerar a estrutura destes ficheiros Pytest rapidamente. O foco do QA é **pensar nos cenários (Análise)**; a codificação (Automação) pode ser agilizada com o uso de Prompts assertivos!

Bom estudo e bons testes! 🐛🔨

---

## 🔍 Revisão com a Skill `prune-tests`

Esta branch (`chore/prune-tests`) aplica a skill **`prune-tests`** (salva em
`~/.config/opencode/skills/prune-tests/SKILL.md`) para auditar e limpar testes
frágeis ou tautológicos. Abaixo, os conceitos que ela ensina.

### Modo de operação: Audit vs Cleanup

A skill separa **o que pedem** de **o que se faz**:

* **Audit** (pedidos como *revisar*, *analisar*, *encontrar*): é somente
  leitura. O resultado é um relatório de disposições — nada é apagado.
* **Cleanup** (pedidos como *podar*, *apagar*, *reescrever*): autoriza as
  edições no escopo aprovado. Invocar a skill sozinha **não** converte uma
  auditoria em limpeza.

O **escopo** fica fixo (um diff, um PR, uma pasta, a suíte inteira) e toda
decisão é tomada **por teste**, nunca por arquivo. Um arquivo só sai depois
que todos os seus testes têm disposição.

### A barra comportamental (6 critérios)

Um teste só sobrevive se passar nos 6 itens — falhar em 1 = recomendar `DELETE`:

1. Prova um comportamento exato vindo de **requisito aprovado**, bug, regra ou
   exemplo trabalhado (**fonte independente**).
2. Detecta uma falha **visível ao usuário ou ao chamador**.
3. O resultado esperado é **independente da implementação**.
4. Observa pelo **contrato público** (interface estável).
5. Sobrevive a **refatores internos** e mudanças de copy/layout incidental.
6. Usa o **menor seam estável** que dá confiança, sem duplicar cobertura
   próxima (domain → application → component → E2E, na camada certa).

### O que a skill manda podar

* **Tautologias** — o esperado é derivado do próprio cálculo de produção
  (ex.: `assert total == valor * 1.1` se a função faz a mesma conta). Passa
  por construção; o esperado precisa poder discordar da implementação.
* **Change detectors** — falham quando o *código* muda, sem apontar
  comportamento errado: scans de fonte (`grep "import x"`), contagens de
  elementos/exports, snapshots de markup/estrutura, asserções sobre
  colaboradores privados, duplicatas cujo único valor é notar mudança.
* **Geometria e aparência** — dimensões, ratios, estilos computados, contagem
  de linhas montadas são evidência visual, não comportamento. Screenshot só
  entra se o projeto adotou regressão visual como requisito.
* **Copy (texto)** — asserção de prosa exata só quando a palavra em si é
  requisito; caso contrário, valide papel, estado, navegação ou *reason code*.
* **Focus/disabled** — mantenha só quando o estado **é** o contrato de
  interação (foco no primeiro campo inválido, Save habilitado após edição).

### Disposições

| Disposição | Quando |
|---|---|
| `DELETE` | Viola a política e nenhum comportamento fica desprotegido. **É o padrão.** |
| `REWRITE` | O teste é inaceitável, mas contém comportamento que passa na barra com justificativa forte. Exceção, não meio-termo. |
| `KEEP` | Suspeito, mas prova comportamento aceitável e passa na barra sem mudar. |

`KEEP` e `REWRITE` exigem **justificativa escrita para os 6 itens** da barra.
Faltando qualquer um, o conselho vira `DELETE`. Ao reescrever, guarda-se
apenas setup/ação/asserções necessárias — não se preserva o tamanho, número
de asserções ou formato do teste antigo.

### Validação e relatório

No cleanup: rodar o menor comando de teste primeiro e depois toda a
validação do repositório; limpar suporte morto (imports, fixtures, helpers);
nunca mudar produção só para preservar um teste; inspecionar o diff final.
O relatório lista `DELETE`/`REWRITE`/`KEEP` com caminho e motivo, a
justificativa completa dos sobreviventes, os comandos executados e qualquer
conflito de política — e declara explicitamente quando não existiu rewrite
aceitável.

### Resultado nesta branch

3 `DELETE` aplicados (duplicata do `ValueError` de saque, teste de isolamento
de fixture que não exercitava a função pública e teste de imutabilidade sem
requisito que o aprovasse), `REWRITE` nenhum, 32 casos `KEEP`, suporte morto
removido (`import copy` órfão) e suíte validada: **74 passed** (−3, exatos
nos removidos).