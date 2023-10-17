var AWS = require('aws-sdk');

exports.handler = async (event) => {
    console.log(JSON.stringify(event))
    const sns = event.Records[0].Sns
    const messsage = JSON.parse(sns.Message)
    
    const shouldAdd = messsage.LifecycleTransition == "autoscaling:EC2_INSTANCE_LAUNCHING"

    var ec2 = new AWS.EC2();
    
    var instanceId = messsage.EC2InstanceId
    console.log(instanceId)
    
    var params = {InstanceIds: [instanceId]}
    console.log(shouldAdd ? 'ADDING':'REMOVING', instanceId)

    const securityGroupId = process.env['SECURITY_GROUP']
    const port = process.env['PORT']

    if(shouldAdd){
        const data = await ec2.describeInstances(params).promise()
        const instanceIp = data.Reservations[0].Instances[0].PrivateIpAddress
        
        var manageParams = {
          GroupId: securityGroupId, 
          IpPermissions: [
             {
            FromPort: port, 
            IpProtocol: "tcp", 
            IpRanges: [
               {
                   CidrIp: instanceIp + "/32",
                   Description: instanceId
               }
            ], 
            ToPort: port
           }
          ]
        };
        
        return await ec2.authorizeSecurityGroupIngress(manageParams).promise()
    }
    
    const group = await ec2.describeSecurityGroups({GroupIds: [securityGroupId]}).promise()
    const ingress = group.SecurityGroups[0].IpPermissions[0].IpRanges.find(i=>i.Description == instanceId)
    
    var manageParams = {
        GroupId: securityGroupId, 
        IpPermissions: [
           {
                FromPort: port, 
                IpProtocol: "tcp", 
                IpRanges: [
                    {
                        CidrIp: ingress.CidrIp,
                        Description: instanceId
                    }
                ],
                ToPort: port
            }
        ]
    };

    return await ec2.revokeSecurityGroupIngress(manageParams).promise()
    
};