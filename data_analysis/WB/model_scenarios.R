
#library
#library(conflicted)  
library(tidyverse)
#conflict_prefer("filter", "dplyr")
#conflict_prefer("lag", "dplyr")

rm(list = ls())

### reading the database
database_raw <- read.csv(paste0(dirname(rstudioapi::getActiveDocumentContext()$path),"/data/SAO_PAULO_PREFERENCIA_DECLARADA_2021_BANCO_03.03.2022_sheet2_treated.csv"), sep=',', check.names=FALSE)

sink(file = "lm_output.txt")

6654/6 #numero de individuos entrevistados
nrow(database_raw)

names(database_raw)  

## Ficha 1 - Modo atual
## Ficha 2 - Bicicleta própria
## Ficha 3 - Bicicleta compartilhada

database <- database_raw %>% 
  mutate(CHOICE = case_when(`Ciclista - PD (Ficha 1 - Selecionado)`=='Selecionado'~1,TRUE~0)) %>% 
  mutate(CHOICE = case_when(`Ciclista - PD (Ficha 2 - Selecionado)`=='Selecionado'~2,TRUE~CHOICE)) %>% 
  mutate(CHOICE = case_when(`Ciclista - PD (Ficha 3 - Selecionado)`=='Selecionado'~3,TRUE~CHOICE)) %>% 
  rename(sexo=`Ciclista - 2. Com qual gênero você se identifica?`,
         faixa_etaria = `Ciclista - 1. Qual a sua idade? (Faixa etária)`,
         classe = `Ciclista - Critério Brasil - Classe`,
         raca = `Ciclista - 19. Com qual cor ou raça você se identifica?`,
         tempo_atual = `Ciclista - PD (Ficha 1 - Tempo de viagem (min))`,
         tempo_bici = `Ciclista - PD (Ficha 2 - Tempo de viagem (min))`,
         tempo_share = `Ciclista - PD (Ficha 3 - Tempo de viagem (min))`,
         bikesp_bici = `Ciclista - PD (Ficha 2 - Remuneracao Bike SP)`,
         bikesp_share = `Ciclista - PD (Ficha 3 - Remuneracao Bike SP)`,
         tempo_acc = `Ciclista - PD (Ficha 3 - Tempo de Acesso (min))`,
         tempo_egr = `Ciclista - PD (Ficha 3 - Tempo de Egresso (min))`,
         cost_atual = `Ciclista - PD (Ficha 1 - Custo (R$))`,
         cost_share = `Ciclista - PD (Ficha 3 - Custo (R$))`,
         infra_bici = `Ciclista - PD (Ficha 2 - Presenca de infraestrutura cicloviária)`,
         infra_share = `Ciclista - PD (Ficha 3 - Presenca de infraestrutura cicloviária)`,
         facilidade_bici = `Ciclista - PD (Ficha 2 - Facilidades no destino)`,
         facilidade_share = `Ciclista - PD (Ficha 3 - Facilidades no destino)`,
         estac_bici = `Ciclista - PD (Ficha 2 - Estacionamento de bicicleta)`,
         infra_bici = `Ciclista - PD (Ficha 2 - Presenca de infraestrutura cicloviária)`,
         infra_share = `Ciclista - PD (Ficha 3 - Presenca de infraestrutura cicloviária)`,
         modo = `Ciclista - 29. Qual o meio de transporte você costumava utilizar para realizar a atividade indicada no item 12 antes da pandemia?`,
         n_morad = `Ciclista - 20. Qual a quantidade de pessoas que moram na sua residência? (Caso more sozinho, assinalar valor igual a 01)`,
         ocupacao = `Ciclista - 24. Qual a sua condição (ocupação) de atividade atual?`,
         renda = `Ciclista - 3. Qual a sua renda familiar?`,
         bici = `Ciclista - 22. Quantas bicicletas estão disponíveis na sua residência?`,
         mot = `Ciclista - 21. Quantos veículos motorizados (Automóvel/Motocicleta) estão disponíveis na sua residência?`,
         modo_princ = `Ciclista - 30. (Modo de transporte principal)`,
         escolaridade = `Ciclista - 18. Qual o seu grau de instrução atual?`,
         idade = `Ciclista - 1. Qual a sua idade?`,
         motivo = `Ciclista - 26. Qual o principal motivo dos seus deslocamentos antes da pandemia?`,
         centro = `Ciclista - 23. Qual o bairro onde você reside? (Area Metro)`
         ) %>% 
  mutate(raca1 = case_when(raca != "1. Branca" ~1,TRUE~0),
         tempo_atual = as.numeric(tempo_atual),
         tempo_bici = as.numeric(tempo_bici),
         tempo_share = as.numeric(tempo_share),
         tempo_acc = as.numeric(tempo_acc),
         tempo_egr = as.numeric(tempo_egr),
         cost_atual = as.numeric(cost_atual),
         cost_share = as.numeric(cost_share),
         bikesp_bici = as.numeric(bikesp_bici),
         bikesp_share = as.numeric(bikesp_share),
         sexo = case_when(sexo == "2. Feminino"~1,TRUE~0),
         classe_2 = case_when(classe == "B2" | classe == "C1"~1,TRUE~0),
         classe_3 = case_when(classe == "C2" |  classe == "DE"~1,TRUE~0),
         tempo_bshare = tempo_share+tempo_acc+tempo_egr,
         bikesp_bici1 = case_when(bikesp_bici > 0 & bikesp_bici <= 2~1,TRUE~0),
         bikesp_bici2 = case_when(bikesp_bici > 2 & bikesp_bici <= 3 ~1,TRUE~0),
         bikesp_bici3 = case_when(bikesp_bici > 3 ~1,TRUE~0),
         bikesp_share1 = case_when(bikesp_share > 0 & bikesp_share <= 2~1,TRUE~0),
         bikesp_share2 = case_when(bikesp_bici > 2 & bikesp_bici <= 3 ~1,TRUE~0),
         bikesp_share3 = case_when(bikesp_share > 3~1,TRUE~0),
         escol_1 = case_when(escolaridade == "3. Fundamental II completo / Médio incompleto" ~1,TRUE~0),
         escol_2 = case_when(escolaridade == "4. Médio Completo / Superior incompleto" |
                               escolaridade == "5. Superior Completo"~1,TRUE~0),
         age_1 = case_when(idade >=18 & idade <40 ~1,TRUE~0),
         age_2 = case_when(idade >40 & idade <65~1,TRUE~0),
         age_3 = case_when(idade >= 65~1,TRUE~0),
         mot_w = case_when(motivo == "1. Trabalho"~1,TRUE~0),
         mot_e = case_when(motivo == "2. Escola / Educação"~1,TRUE~0),
         mot_o = case_when(motivo != "2. Escola / Educação" | motivo != "1. Trabalho"~1,TRUE~0),
         infra_bici1 = case_when(infra_bici != "Sem Ciclovia"~1,TRUE~0),
         infra_share1 = case_when(infra_share != "Sem Ciclovia"~1,TRUE~0),
         estac_bici1 = case_when(estac_bici == "Bicicletário com monitoramento"~1,TRUE~0),
         estac_bici2 = case_when(estac_bici == "Bicicletário sem monitoramento"~1,TRUE~0),
         facilidade_bici = case_when(facilidade_bici == "Sim"~1,TRUE~0),
         facilidade_share = case_when(facilidade_share == "Sim"~1,TRUE~0),
         bici = case_when(bici != "1. Nenhum" ~1,TRUE~0),
         mot = case_when(mot != "1. Nenhum" ~1,TRUE~0),
         centro = case_when(centro == "9-Centro"~1,TRUE~0),
         n_morad = as.numeric(n_morad)
  )

prop.table(table(database$CHOICE)) ## proporção de participantes por ficha


database <- database %>%
  filter(cost_atual < 60)


# database <- database[,-1]  ## aqui está removendo a coluna Cenario (não faz sentido)

#renomeando a variavel de identificador unico e rearranjando
database <- database %>% 
  rename(ID=`Ciclista - hash_unico`) %>% 
  arrange(ID)

length(unique(database$ID)) #numero de ID unicos

data <- database

#analise descritiva
data <- database %>% 
  filter(Cenario == 1) 

str(database)

mean(database$tempo_atual)
quantile(database$tempo_atual)
mean(database$tempo_bici)
quantile(database$tempo_bici)
mean(database$tempo_bshare)
quantile(database$tempo_bshare)

###TABELAS
table(data$`Ciclista - Usuario realizou pesquisa`,useNA = 'always')

table(data$idade,useNA = 'always')
prop.table(table(data$idade,useNA = 'always'))*100

prop.table(table(database$renda,useNA = 'always'))*100

prop.table(table(data$faixa_etaria))*100

prop.table(table(database$CHOICE))*100

data$idade <- as.numeric(data$idade)

quantile(data$idade)

table(data$renda,useNA = 'always')
prop.table(table(data$sexo,useNA = 'always'))


unique(database$modo)

table(database$modo,useNA = 'always')

prop.table(table(database$ocupacao,useNA = 'always'))*100
prop.table(table(database$bici,useNA = 'always'))*100
prop.table(table(database$mot,useNA = 'always'))*100
prop.table(table(database$CHOICE,useNA = 'always'))*100

prop.table(table(data$classe,useNA = 'always'))*100
prop.table(table(data$raca,useNA = 'always'))*100

quantile(database$cost_share)
quantile(database$cost_atual)
quantile(database$bikesp_bici)
quantile(database$bikesp_share)
quantile(database$tempo_atual)

prop.table(table(data$motivo,useNA = 'always'))*100

unique(database_raw$`Ciclista - 23. Qual o bairro onde você reside? (Area Metro)`)
unique(database_raw$`Ciclista - 23. Qual o bairro onde você reside? (Area SPTrans)`)

a <- psych::describe(database)

range(database$infra_bici)

database <- database[c("ID", "CHOICE", "tempo_atual", "cost_atual", "tempo_bici", "infra_bici1", "bikesp_bici1", "bikesp_bici2", "estac_bici1", "estac_bici2",
                        "facilidade_bici", "sexo", "classe_2", "classe_3", "n_morad", "bici", "mot", "age_2", "age_3", "mot_w", "mot_e", "centro",
                        "raca1", "tempo_share", "cost_share", "tempo_acc", "tempo_egr", "infra_share1", "bikesp_share1", "bikesp_share2", "facilidade_share",
                        "sexo", "classe_2", "classe_3", "n_morad", "bici", "mot", "age_2", "age_3", "mot_w", "mot_e", "centro", "raca1")]

database <- database[order(database$ID),]

database <- as.data.frame(database)

################# MODELO #####################

### Load Apollo library
library(apollo)

# ################################################################# #
#### LOAD DATA AND APPLY ANY TRANSFORMATIONS                     ####
# ################################################################# #
choiceAnalysis_settings <- list(
  alternatives = c(atual=1,bici=2,share=3),
  avail        = list(atual=1,bici=1,share=1),
  choiceVar    = database$CHOICE,
  explanators  = database[,c("sexo")])

### Initialise code
apollo_initialise()

### Set core controls
apollo_control = list(
  modelName    = 'mnl_rum_final ',
  modelDescr   = "MNL RUM model",
  indivID      = "ID",
  outputDirectory = paste0(dirname(rstudioapi::getActiveDocumentContext()$path),'/resultados/')
)
apollo_choiceAnalysis(choiceAnalysis_settings, apollo_control, database)
# ################################################################# #
#### DEFINE MODEL PARAMETERS                                     ####
# ################################################################# #

### Vector of parameters, including any that are kept fixed in estimation
apollo_beta = c(asc_atual     = 0,
                asc_bici      = 0,
                asc_share     = 0,
                b_tempo       = 0,
                b_tempo_mile  = 0,
                b_cost_atual             = 0,
                b_cost_share             = 0,
                b_infra            = 0,
                b_bikesp1           = 0,
                b_bikesp2           = 0,
                b_estac1            = 0,
                b_estac2            = 0,
                b_facil_bici            = 0,
                b_facil_share            = 0,
                b_sexo             = 0,
                b_classeb          = 0,
                b_classecde        = 0,
                b_nmorad           = 0,
                b_nbici_bici            = 0,
                b_nbici_share           = 0,
                b_nmot              = 0,
                b_age2            = 0,
                b_age3            = 0,
                b_motw            = 0,
                b_mote            = 0,
                b_centro          = 0,
                b_raca            = 0
)

### Vector with names (in quotes) of parameters to be kept fixed at their starting value in apollo_beta, use apollo_beta_fixed = c() if none
apollo_fixed = c("asc_atual")

# ################################################################# #
#### GROUP AND VALIDATE INPUTS                                   ####
# ################################################################# #

apollo_inputs = apollo_validateInputs()

# ################################################################# #
#### DEFINE MODEL AND LIKELIHOOD FUNCTION                        ####
# ################################################################# #

apollo_probabilities=function(apollo_beta, apollo_inputs, functionality="estimate"){
  
  ### Attach inputs and detach after function exit
  apollo_attach(apollo_beta, apollo_inputs)
  on.exit(apollo_detach(apollo_beta, apollo_inputs))
  
  ### Create list of probabilities P
  P = list()
  
  
  ### List of utilities: these must use the same names as in mnl_settings, order is irrelevant
  V = list()
  
  V[['atual']]  =  asc_atual + b_tempo*tempo_atual + b_cost_atual*cost_atual
  
  V[['bici']]  = asc_bici + b_tempo*tempo_bici + 
    b_infra*infra_bici1  +
    b_bikesp1*bikesp_bici1 + b_bikesp2*bikesp_bici2 + 
    b_estac1*estac_bici1 + b_estac2*estac_bici2 + 
    b_facil_bici*facilidade_bici +
    b_sexo*sexo + b_classeb*classe_2 + b_classecde*classe_3 + b_nmorad*n_morad + b_nbici_bici*bici +
    b_nmot*mot + b_age2*age_2 + b_age3*age_3 +
    b_motw*mot_w + b_mote*mot_e + b_centro*centro + b_raca*raca1
  
  V[['share']] = asc_share + b_tempo*tempo_share + b_cost_share*cost_share + 
    b_tempo_mile*tempo_acc + b_tempo_mile*tempo_egr + 
    b_infra*infra_share1 + 
    b_bikesp1*bikesp_share1 + b_bikesp2*bikesp_share2 + 
    b_facil_share*facilidade_share +
    b_sexo*sexo + b_classeb*classe_2 + b_classecde*classe_3 + b_nmorad*n_morad + b_nbici_share*bici +
    b_nmot*mot + b_age2*age_2 + b_age3*age_3 +
    b_motw*mot_w + b_mote*mot_e + b_centro*centro + b_raca*raca1
  
  ### Define settings for MNL model component
  mnl_settings = list(
    alternatives = c(atual=1,bici=2,share=3),
    avail        = list(atual=1,bici=1,share=1),
    choiceVar    = CHOICE,
    V            = V
  )
  
  ### Compute probabilities using MNL model
  P[['model']] = apollo_mnl(mnl_settings, functionality)
  
  #repeat individuals
  P = apollo_panelProd(P,apollo_inputs,functionality)
  
  ### Prepare and return outputs of function
  P = apollo_prepareProb(P, apollo_inputs, functionality)
  return(P)
}

# ################################################################# #
#### MODEL ESTIMATION                                            ####
# ################################################################# #

model_mnl  <-  apollo_estimate(apollo_beta, apollo_fixed, apollo_probabilities, apollo_inputs, 
                                estimate_settings = list(printLevel = 3))

# ################################################################# #
#### MODEL OUTPUTS                                               ####
# ################################################################# #

apollo_modelOutput(model_mnl, modelOutput_settings = list(printClassical = TRUE,printPVal = TRUE))

# ----------------------------------------------------------------- #
#---- FORMATTED OUTPUT (TO FILE, using model name)               ----
# ----------------------------------------------------------------- #

apollo_saveOutput(model_mnl,saveOutput_settings = list(printPVal=T ,printT1=T,
                                                        printDiagnostics = T)) #ver saveoutput list para mais configuracoes

#apollo_lrTest(model_mnl1,model_mnl2) ## não faz sentido essa parte estar aqui

########### Elasticity ##################
#                                       #
#########################################
model <- model_mnl

predictions_base <- apollo_prediction(model_mnl,apollo_probabilities,apollo_inputs,
                                      prediction_settings = list(runs=1))

summary(predictions_base)

#elasticity bikeSP bici 2
database$bikesp_bici_real <- database$bikesp_bici2

database$bikesp_bici2 <- 1

apollo_inputs = apollo_validateInputs()

prediction_bikesp1 <- apollo_prediction(model_mnl,apollo_probabilities,apollo_inputs,
                                      prediction_settings = list(runs=1))

database$bikesp_bici2 <- 0

apollo_inputs = apollo_validateInputs()

prediction_bikesp2 <- apollo_prediction(model_mnl,apollo_probabilities,apollo_inputs,
                                      prediction_settings = list(runs=1))

database$bikesp_bici2 <- database$bikesp_bici_real
apollo_inputs = apollo_validateInputs()

mean(prediction_bikesp1$bici-prediction_bikesp2$bici)*100

########### bikeSP - BICI - 1
database$bikesp_bici_df1 <- database$bikesp_bici1

database$bikesp_bici1 <- 1

apollo_inputs = apollo_validateInputs()

prediction_bikesp_bici11 <- apollo_prediction(model_mnl,apollo_probabilities,apollo_inputs,
                                      prediction_settings = list(runs=1))

database$bikesp_bici1 <- 0

apollo_inputs = apollo_validateInputs()

prediction_bikesp12 <- apollo_prediction(model_mnl,apollo_probabilities,apollo_inputs,
                                      prediction_settings = list(runs=1))

database$bikesp_bici1 <- database$bikesp_bici_df1
apollo_inputs = apollo_validateInputs()

mean(prediction_bikesp_bici11$bici-prediction_bikesp12$bici)*100


###########
database$bikesp_share_df1 <- database$bikesp_share1

database$bikesp_share1 <- 1

apollo_inputs = apollo_validateInputs()

prediction_bikesp_share11 <- apollo_prediction(model_mnl,apollo_probabilities,apollo_inputs,
                                      prediction_settings = list(runs=1))

database$bikesp_share1 <- 0

apollo_inputs = apollo_validateInputs()

prediction_bikesp_share12 <- apollo_prediction(model_mnl,apollo_probabilities,apollo_inputs,
                                      prediction_settings = list(runs=1))

database$bikesp_share1 <- database$bikesp_share_df1
apollo_inputs = apollo_validateInputs()

mean(prediction_bikesp_share11$share-prediction_bikesp_share12$share)*100

###########
database$bikesp_share_df2 <- database$bikesp_share2

database$bikesp_share2 <- 1

apollo_inputs = apollo_validateInputs()

prediction_bikesp_share21 <- apollo_prediction(model_mnl,apollo_probabilities,apollo_inputs,
                                               prediction_settings = list(runs=1))

database$bikesp_share2 <- 0

apollo_inputs = apollo_validateInputs()

prediction_bikesp_share22 <- apollo_prediction(model_mnl,apollo_probabilities,apollo_inputs,
                                               prediction_settings = list(runs=1))

database$bikesp_share2 <- database$bikesp_share_df2
apollo_inputs = apollo_validateInputs()

mean(prediction_bikesp_share21$share-prediction_bikesp_share22$share)*100

### elasticity cost sharing ##
predictions_base = apollo_prediction(model_mnl, apollo_probabilities, apollo_inputs)

elast_coshare <- (1-predictions_base[,'share'])*model_mnl$estimate[['b_cost_share']]*database$cost_share
agg_coshare <- sum(elast_coshare*(predictions_base[,'share']/sum(predictions_base[,'share'])))

mean(agg_coshare)

database$cost_share <- 1.01*database$cost_share
apollo_inputs = apollo_validateInputs()
predictions_costshare = apollo_prediction(model_mnl, apollo_probabilities, apollo_inputs,
                                          prediction_settings = list(runs=1))

database$cost_share <- 1/1.01*database$cost_share
apollo_inputs = apollo_validateInputs()

predictions_base <- predictions_base[,3:5]
predictions_costshare <- predictions_costshare[,3:5]

change=(predictions_costshare-predictions_base)/predictions_base
summary(change)
colMeans(change,na.rm=TRUE)

#log(sum(predictions_costshare[,5])/sum(predictions_base[,5]))/log(1.01) ## aqui não parece fazer sentido visto que tem apenas 3 colunas (atual, bici e share)

########################### infra elasticity
database$infra_bici_df <- database$infra_bici1

database$infra_bici1 <- 1
apollo_inputs = apollo_validateInputs()

prediction_infra_bici11 <- apollo_prediction(model_mnl,apollo_probabilities,apollo_inputs,
                                        prediction_settings = list(runs=1))

database$infra_bici1 <- 0
apollo_inputs = apollo_validateInputs()

prediction_infra_bici12 <- apollo_prediction(model_mnl,apollo_probabilities,apollo_inputs,
                                        prediction_settings = list(runs=1))

database$infra_bici1 <- database$infra_bici_df
apollo_inputs = apollo_validateInputs()

mean(prediction_infra_bici11$bici-prediction_infra_bici12$bici)*100

########################### infra elasticity
database$infra_share_df <- database$infra_share1

database$infra_share1 <- 1
apollo_inputs = apollo_validateInputs()

prediction_infra_share11 <- apollo_prediction(model_mnl,apollo_probabilities,apollo_inputs,
                                       prediction_settings = list(runs=1))

database$infra_share1 <- 0
apollo_inputs = apollo_validateInputs()

prediction_infra_share12 <- apollo_prediction(model_mnl,apollo_probabilities,apollo_inputs,
                                       prediction_settings = list(runs=1))

database$infra_share1 <- database$infra_share_df
apollo_inputs = apollo_validateInputs()

mean(prediction_infra_share11$share-prediction_infra_share12$share)*100

########################### parking elasticity
database$estac1_df <- database$estac_bici1

database$estac_bici1 <- 1
apollo_inputs = apollo_validateInputs()

prediction_estac_bici11 <- apollo_prediction(model_mnl,apollo_probabilities,apollo_inputs,
                                             prediction_settings = list(runs=1))

database$estac_bici1 <- 0
apollo_inputs = apollo_validateInputs()

prediction_estac_bici12 <- apollo_prediction(model_mnl,apollo_probabilities,apollo_inputs,
                                             prediction_settings = list(runs=1))

database$estac_bici1 <- database$estac1_df
apollo_inputs = apollo_validateInputs()

mean(prediction_estac_bici11$bici-prediction_estac_bici12$bici)*100

########################### infra elasticity
database$estac2_df <- database$estac_bici2

database$estac_bici2 <- 1
apollo_inputs = apollo_validateInputs()

prediction_estac_bici21 <- apollo_prediction(model_mnl,apollo_probabilities,apollo_inputs,
                                             prediction_settings = list(runs=1))

database$estac_bici2 <- 0
apollo_inputs = apollo_validateInputs()

prediction_estac_bici22 <- apollo_prediction(model_mnl,apollo_probabilities,apollo_inputs,
                                             prediction_settings = list(runs=1))

database$estac_bici2 <- database$estac2_df
apollo_inputs = apollo_validateInputs()

mean(prediction_estac_bici21$bici-prediction_estac_bici22$bici)*100

########################### facilities elasticity
database$facilidade_bici_df <- database$facilidade_bici

database$facilidade_bici <- 1
apollo_inputs = apollo_validateInputs()

prediction_facilidade1 <- apollo_prediction(model_mnl,apollo_probabilities,apollo_inputs,
                                             prediction_settings = list(runs=1))

database$facilidade_bici <- 0
apollo_inputs = apollo_validateInputs()

prediction_facilidade2 <- apollo_prediction(model_mnl,apollo_probabilities,apollo_inputs,
                                             prediction_settings = list(runs=1))

database$facilidade_bici <- database$facilidade_bici_df
apollo_inputs = apollo_validateInputs()

mean(prediction_facilidade1$bici-prediction_facilidade2$bici)*100

########################### facilities elasticity
database$facilidade_share_df <- database$facilidade_share

database$facilidade_share <- 1
apollo_inputs = apollo_validateInputs()

prediction_facilidade_share1 <- apollo_prediction(model_mnl,apollo_probabilities,apollo_inputs,
                                            prediction_settings = list(runs=1))

database$facilidade_share <- 0
apollo_inputs = apollo_validateInputs()

prediction_facilidade_share2 <- apollo_prediction(model_mnl,apollo_probabilities,apollo_inputs,
                                            prediction_settings = list(runs=1))

database$facilidade_share <- database$facilidade_share_df
apollo_inputs = apollo_validateInputs()

mean(prediction_facilidade_share1$share-prediction_facilidade_share2$share)*100

sink(file = NULL)

#################### 
database <- read_csv("20220125_database_final.csv") #OD LUCAS  ## não obtive acesso a esse arquivo, portanto dessa linha para baixo do código não foi possível analisar nada

database <- database[,-c(1:2)] #elimiando duas primeiras colunas

database <- database %>% 
  mutate(dist_infrao = case_when((dist_o_ciclovia < dist_o_ciclofaixas) == T~dist_o_ciclovia, TRUE~dist_o_ciclofaixas)) %>% 
  mutate(dist_infrad = case_when((dist_d_ciclovia < dist_d_ciclofaixas) == T~dist_d_ciclovia, TRUE~dist_d_ciclofaixas)) %>% 
  mutate(infrao = case_when(dist_infrao <= 500~1,TRUE~0)) %>% 
  mutate(infrad = case_when(dist_infrad <= 500~1,TRUE~0)) %>% 
  mutate(infrao_28 = case_when(dist_o_infra_2028 <= 500~1,TRUE~0)) %>% 
  mutate(infrad_28 = case_when(dist_d_infra_2028 <= 500~1,TRUE~0)) %>% 
  rename(perc_atual = '%_route_covered_atual',
         perc_2028 = '%_route_covered_2028') %>% 
  mutate(perc_atual = perc_atual/100,
         perc_2028 = perc_2028/100) %>% 
  mutate(modo = case_when(modoprin <=5 ~1,TRUE~0)) %>% 
  mutate(modo = case_when(modoprin ==9 ~2,TRUE~modo)) %>% 
  mutate(modo = case_when(modoprin ==15 ~3,TRUE~modo))


database <- database %>% 
  rename(
         estac_bici1 = bicic_d,
         mot_e = motiv2 ,
         mot_w = motiv1,
         bici = qt_bicicle,
         centro = mini_anel,
         ID = id_pess,
         n_morad = no_morad) %>% 
  mutate(tempo_atual = 0,
         tempo_bici = time_bici,
         tempo_share = 0,
         tempo_acc = 0,
         tempo_egr = 0,
         bikesp_bici1 = 0,
         bikesp_bici2 = 0,
         bikesp_share1 = 0,
         bikesp_share2 = 0,
         facilidade_share = 0,
         facilidade_bici = 0,
         CHOICE = case_when(choice == 1~2,TRUE~0),
         CHOICE = case_when(choice == 0~1,TRUE~CHOICE),
         mot = case_when(qt_auto+qt_moto>1~1,TRUE~0),
         classe_2 = case_when(criteriobr == 3 | criteriobr == 4~1,TRUE~0),
         classe_3 = case_when(criteriobr == 5 |  criteriobr == 6~1,TRUE~0),
         age_1 = case_when(idade >=18 & idade <40 ~1,TRUE~0),
         age_2 = case_when(idade >40 & idade <65~1,TRUE~0),
         age_3 = case_when(idade >= 65~1,TRUE~0),
         infra_share1 = case_when(infrao == 1 & infrad == 1~1,TRUE~0),
         infra_bici1 = case_when(infrao == 1 & infrad == 1~1,TRUE~0),
         infra_sharefut = case_when(infrao_28 == 1 & infrad_28 == 1~1,TRUE~0),
         infra_bicifut = case_when(infrao_28 == 1 & infrad_28 == 1~1,TRUE~0),
         cost_atual = 0,
         cost_share = 0,
         estac_bici2 = estac_bici1,
         raca1 = 0
         ) %>% 
  arrange(ID)

########### Elasticity ##################
#                                       #
#########################################
model_mnl <- model

apollo_inputs = apollo_validateInputs()

predictions_od <- apollo_prediction(model_mnl,apollo_probabilities,apollo_inputs,
                                      prediction_settings = list(runs=1))

summary(predictions_base)

prop.table(table(database$CHOICE))*100

model_mnl$estimate["asc_atual"]=model_mnl$estimate["asc_atual"]+log(.93/.34)
model_mnl$estimate["asc_bici"]=model_mnl$estimate["asc_bici"]+log(.064/.48)
model_mnl$estimate["asc_share"]=model_mnl$estimate["asc_share"]+log(.001/.18)

predictions_od <- apollo_prediction(model_mnl,apollo_probabilities,apollo_inputs,
                                    prediction_settings = list(runs=1))

model_mnl$estimate["asc_atual"]=model_mnl$estimate["asc_atual"]+log(.93/.92)
model_mnl$estimate["asc_bici"]=model_mnl$estimate["asc_bici"]+log(.064/.08)
model_mnl$estimate["asc_share"]=model_mnl$estimate["asc_share"]+log(.001/.01)
predictions_od <- apollo_prediction(model_mnl,apollo_probabilities,apollo_inputs,
                                    prediction_settings = list(runs=1))

model_mnl$estimate["asc_atual"]=model_mnl$estimate["asc_atual"]+log(.93/.93)
model_mnl$estimate["asc_bici"]=model_mnl$estimate["asc_bici"]+log(.064/.07)
model_mnl$estimate["asc_share"]=model_mnl$estimate["asc_share"]+log(.001/.01)
predictions_od <- apollo_prediction(model_mnl,apollo_probabilities,apollo_inputs,
                                    prediction_settings = list(runs=1))

summary(predictions_od)

#### mudança
database$infra_bici1_old <- database$infra_bici1

database$infra_bici1 <- database$infra_bicifut

apollo_inputs = apollo_validateInputs()

predictions_od1 <- apollo_prediction(model_mnl,apollo_probabilities,apollo_inputs,
                                    prediction_settings = list(runs=1))

database$infra_bici1 <- database$infra_bici1_old
apollo_inputs = apollo_validateInputs()

mean(predictions_od1$bici-predictions_od$bici)*100


############
set.seed(123)

database$infra_bici1_old <- database$infra_bici1
database$estac_bici1_old <- database$estac_bici1
database$facilidade_bici_old <- database$facilidade_bici
database$bikesp_bici1_old <- database$bikesp_bici1
database$bikesp_bici2_old <- database$bikesp_bici2

mean(database$estac_bici1)
mean(database$facilidade_bici)
mean(database$facilidade_bici)

database <- database %>% 
  mutate(infra_bici1 = infra_bicifut) %>% 
  mutate(estac_bici1 = case_when(estac_bici1 == 0~ifelse(runif(nrow(database),min = 0,max = 1)<0.50,1,0),TRUE~estac_bici1)) %>% 
  mutate(facilidade_bici = case_when(facilidade_bici == 0~ifelse(runif(nrow(database))<0.40,1,0),TRUE~facilidade_bici)) %>% 
  mutate(bikesp_bici1 = case_when(bikesp_bici1 == 0 & mot_e == 1~ifelse(runif(nrow(database))<0.50,1,0),TRUE~bikesp_bici1)) %>% 
  mutate(bikesp_bici2 = case_when(bikesp_bici2 == 0 & mot_e == 1~ifelse(runif(nrow(database))<0.20,1,0),TRUE~bikesp_bici2))

database[9821,c('estac_bici1_old','estac_bici1')]

mean(database$estac_bici1)
mean(database$facilidade_bici)
mean(database$bikesp_bici1)
mean(database$bikesp_bici2)

apollo_inputs = apollo_validateInputs()

predictions_od1 <- apollo_prediction(model_mnl,apollo_probabilities,apollo_inputs,
                                     prediction_settings = list(runs=1))

database$infra_bici1 <- database$infra_bici1_old
database$estac_bici1 <- database$estac_bici1_old
database$facilidade_bici <- database$facilidade_bici
database$bikesp_bici1 <- database$bikesp_bici1_old
database$bikesp_bici2 <- database$bikesp_bici2_old

apollo_inputs = apollo_validateInputs()

mean(predictions_od1$bici-predictions_od$bici)*100

############
set.seed(123)

database <- database %>% 
  mutate(infra_bici1 = infra_bicifut) %>% 
  mutate(estac_bici1 = case_when(estac_bici1 == 0~ifelse(runif(nrow(database))<0.30,1,0),TRUE~estac_bici1)) %>% 
  mutate(facilidade_bici = case_when(facilidade_bici == 0~ifelse(runif(nrow(database))<0.20,1,0),TRUE~facilidade_bici)) %>% 
  mutate(bikesp_bici1 = case_when(bikesp_bici1 == 0~ifelse(runif(nrow(database))<0.20,1,0),TRUE~bikesp_bici1)) %>% 
  mutate(bikesp_bici2 = case_when(bikesp_bici2 == 0~ifelse(runif(nrow(database))<0.10,1,0),TRUE~bikesp_bici2))

mean(database$estac_bici1)
mean(database$facilidade_bici)
mean(database$bikesp_bici1)
mean(database$bikesp_bici2)

apollo_inputs = apollo_validateInputs()

predictions_od1 <- apollo_prediction(model_mnl,apollo_probabilities,apollo_inputs,
                                     prediction_settings = list(runs=1))

database$infra_bici1 <- database$infra_bici1_old
database$estac_bici1 <- database$estac_bici1_old
database$facilidade_bici <- database$facilidade_bici_old
database$bikesp_bici1 <- database$bikesp_bici1_old
database$bikesp_bici2 <- database$bikesp_bici2_old

apollo_inputs = apollo_validateInputs()

mean(predictions_od1$bici-predictions_od$bici)*100


############ ODDS RATIO

(exp(model_mnl$estimate['b_sexo'])-1)*100
(exp(model_mnl$estimate['b_mote'])-1)*100
(exp(model_mnl$estimate['b_motw'])-1)*100
(exp(model_mnl$estimate['b_classeb'])-1)*100
(exp(model_mnl$estimate['b_classecde'])-1)*100
(exp(model_mnl$estimate['b_age3'])-1)*100
(exp(model_mnl$estimate['b_age2'])-1)*100

(exp(model_mnl$estimate['b_infra'])-1)
(exp(model_mnl$estimate['b_raca'])-1)*100
(exp(model_mnl$estimate['b_cost_share'])-1)*100
(exp(model_mnl$estimate['b_bikesp1'])-1)*100
(exp(model_mnl$estimate['b_bikesp2'])-1)*100
(exp(model_mnl$estimate['b_estac1'])-1)*100
(exp(model_mnl$estimate['b_facil_bici'])-1)*100
(exp(model_mnl$estimate['b_facil_share'])-1)*100
(exp(model_mnl$estimate['b_nmorad'])-1)*100
(exp(model_mnl$estimate['b_nbici_bici'])-1)*100
(exp(model_mnl$estimate['b_nbici_share'])-1)*100
(exp(model_mnl$estimate['b_nmot'])-1)*100

