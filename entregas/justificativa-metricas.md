# Justificativa das métricas — Dashboard 2: Pinguins Palmer

**Público-alvo:** estudantes, professores e pessoas que exploram a amostra de pinguins do Arquipélago Palmer. Os registros foram coletados entre 2007 e 2009. As métricas descrevem a base tratada e o recorte escolhido; não representam toda a população de pinguins.

**Filtros:** espécie e ilha. O gráfico de barras pode agrupar por espécie ou por ilha. Clicar em uma barra restringe os quatro indicadores e o gráfico de massa média ao grupo escolhido; dar clique duplo limpa a seleção. Os dois filtros e a seleção devem ser considerados juntos. A contagem é sempre mostrada para indicar o tamanho do recorte.

## 1. Registros selecionados

- **Variável:** contagem de linhas da base tratada.
- **O que mede:** quantidade de registros após filtros e eventual seleção de uma barra.
- **Por que foi escolhida:** mostra o tamanho da amostra usada nos demais indicadores.
- **Público-alvo:** quem compara grupos da amostra.
- **Decisão apoiada:** verificar se um grupo tem registros suficientes para merecer comparação ou se precisa de mais observações.
- **O que comunica:** quantos pinguins compõem o recorte apresentado; contagens pequenas exigem cuidado.

## 2. Massa corporal média

- **Variável:** `body_mass_g`, em gramas.
- **O que mede:** média aritmética da massa dos registros selecionados.
- **Por que foi escolhida:** é uma medida física simples e permite comparar o porte entre grupos.
- **Público-alvo:** pessoas interessadas em características físicas das espécies.
- **Decisão apoiada:** escolher quais grupos comparar em gráficos ou investigar com maior detalhe.
- **O que comunica:** a massa média observada no recorte, que pode ser influenciada por valores extremos e composição por espécie e sexo.

## 3. Comprimento médio da nadadeira

- **Variável:** `flipper_length_mm`, em milímetros.
- **O que mede:** média aritmética do comprimento da nadadeira dos registros selecionados.
- **Por que foi escolhida:** a EDA identificou relação positiva entre essa medida e a massa corporal.
- **Público-alvo:** estudantes investigando diferenças de tamanho entre grupos.
- **Decisão apoiada:** selecionar grupos para comparar com a massa ou aprofundar a análise da relação entre as medidas.
- **O que comunica:** o comprimento médio observado da nadadeira no recorte, sem afirmar relação de causa e efeito.

## 4. Proporção de Gentoo

- **Variável:** `species`.
- **O que mede:** 100 × número de registros Gentoo / número de registros no recorte.
- **Por que foi escolhida:** indica quanto a composição por espécie pode influenciar os resultados agregados; Gentoo tem maior massa média nesta amostra.
- **Público-alvo:** quem interpreta médias e compara espécies ou ilhas.
- **Decisão apoiada:** perceber quando é útil analisar os grupos separadamente antes de interpretar uma média geral.
- **O que comunica:** percentual de Gentoo **na amostra filtrada**, não uma proporção da população natural. Se o recorte não tem registros, a porcentagem não é calculada.

## Visualizações e limites

O gráfico de barras mostra a contagem por espécie ou ilha. A segunda visualização compara a massa média por espécie e indica a quantidade de registros de cada grupo no tooltip. Ambos usam a mesma seleção; os indicadores usam o mesmo recorte. O mapa de calor e o histograma pertencem ao Dashboard 1.

A amostra não representa toda a Antártida. As espécies não foram registradas igualmente em todas as ilhas: Chinstrap aparece apenas em Dream e Gentoo apenas em Biscoe. Por isso, diferenças entre ilhas não podem ser atribuídas à localização isoladamente. Os dois registros sem medidas físicas foram excluídos do conjunto tratado e nove registros têm sexo não informado.
