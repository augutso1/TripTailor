# TripTailor

TripTailor é um planejador de viagens inteligente que utiliza IA para criar roteiros personalizados com base nas suas preferências.

## Funcionalidades

- Geração de itinerários personalizados com base em preferências (pontos turísticos, gastronomia, natureza)
- Otimização de rotas para minimizar deslocamentos
- Recomendações baseadas em distância e preferências do usuário
- Interface de linha de comando simples e intuitiva

## Tecnologias Utilizadas

- Python
- Requests (para chamadas de API)
- API de Geolocalização: Geoapify

## Configuração

### API Keys

O projeto utiliza a API Geoapify para geocodificação e busca de locais. Você precisa obter uma chave de API:

1. Crie uma conta em [Geoapify](https://www.geoapify.com/)
2. Obtenha sua chave de API gratuita
3. Crie um arquivo `.env` na raiz do projeto (use o arquivo `.env.example` como modelo)
4. Adicione sua chave de API ao arquivo `.env`:
   ```
   GEOAPIFY_API_KEY=sua_chave_api_aqui
   ```

## Como Executar

1. Clone o repositório
2. Ative o ambiente virtual:
   ```
   source venv/bin/activate
   ```
3. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```
4. Configure as variáveis de ambiente (veja a seção "Configuração")
5. Execute o programa:
   ```
   python main.py
   ```
6. Siga as instruções no terminal para inserir seu destino, hotel, duração e preferências

## Estrutura do Projeto

- `main.py`: Lógica principal do gerador de itinerários
- `.env`: Arquivo de variáveis de ambiente (não versionado)
- `.env.example`: Exemplo de arquivo de variáveis de ambiente

## Exemplo de Uso

```
$ python main.py
Destino: Paris, França
Hotel: Hotel de Ville
Duração (dias): 3
Preferência (ex: mais pontos turísticos, foco em gastronomia): mais pontos turísticos

Plano de Viagem para Paris, França - 3 dias
Hotel: Hotel de Ville

Dia 1:
- Manhã: Torre Eiffel (Tourism Attraction) - Distância do ponto anterior: 4.32 km
- Tarde: Museu do Louvre (Tourism Attraction) - Distância do ponto anterior: 2.15 km
- Noite: Catedral de Notre-Dame (Tourism Attraction) - Distância do ponto anterior: 1.28 km

Dia 2:
...

Resumo:
- Total de locais visitados: 9
```

## Licença

Este projeto está licenciado sob a licença MIT.
