/* get Marca */
$(function() {
    $("#id_marca_id").change(function(){
      var select = document.getElementById('id_marca_id');
      var value_marca = select.options[select.selectedIndex].text;
      document.getElementById('marca').value=value_marca;
    })
  })
  
  /* get uf*/  
  $(function() {
    $("#id_uf").change(function(){
      var select = document.getElementById('id_uf');
      var value = select.options[select.selectedIndex].value;
      getCidades(value)
    })
  })
  /* get url */
  /* 
  https://servicodados.ibge.gov.br/api/v1/localidades/estados 
  https://servicodados.ibge.gov.br/api/v1/localidades/estados/{uf_ref}/municipios
    */ 
  
  function getCidades(cidade) {
    let xhr = new XMLHttpRequest();
    xhr.open('GET', `https://servicodados.ibge.gov.br/api/v1/localidades/estados/${cidade}/municipios`);
    
    xhr.setRequestHeader('Content-Type', 'application/json;charset=UTF-8');
    
  let cidadesSelect = document.getElementById('id_cidade');
    /*
    xhr.onprogress = function(){
      console.log("Carregando...");
    }
    */
    cidadesSelect.options.length = 0;
    
    xhr.onload = function(){
  
      let cidades = JSON.parse(xhr.responseText);
      
          
      //cidadesSelect.options.length = 0;
      for(cidade in cidades) {
        //console.log(cidades[cidade].nome);
        option = new Option(cidades[cidade].nome);
        cidadesSelect.options[cidadesSelect.options.length] = option;
      }
      //console.log(data);
    }
    xhr.send();
  }