export function normalizeConnections(raw){
 if(!raw)return null;
 const result={};
 for(const [key,field,method] of [['upstream','prev','gradient_x_activation'],['downstream','next','zero_ablation_effect']]){
  const side=raw[field];result[key]={source_layer:key==='upstream'?side?.layer:null,target_layer:key==='downstream'?side?.layer:null,method,positive:(side?.pos||[]).slice(0,4).map(row=>({neuron:row[0],value:row[1],sample_count:row[2],example_count:row[3]})),negative:(side?.neg||[]).slice(0,4).map(row=>({neuron:row[0],value:row[1],sample_count:row[2],example_count:row[3]}))};
 }return result;
}
export function normalizeNeuron(layer,n,connections){
 const s=n.s;return {layer,neuron:n.c,source_verified:true,raw:n,activation_statistics:{maximum:s.max,p99_99:s.p9999,p99_9:s.p999,p99:s.p99,median:s.p50,active_image_percent:s.active*100,pre_relu_minimum:s.nmin,pre_relu_p0_1:s.n001,mean:s.mean,std:s.std,pre_relu_p1:s.n01,pre_relu_mean:s.nmean},top60_classes:(n.cls||[]).map(([label,count])=>({label,count})),connections:normalizeConnections(connections)};
}
