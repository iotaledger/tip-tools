# -*- coding: utf-8 -*-

#===============================================================================
# returns the maximum possible size of a payload
def getPayloadSizeMax(block_size_max):
    payload_size_max = block_size_max
    payload_size_max -= 1               # ProtocolVersion
    payload_size_max -= 1               # ParentCount
    payload_size_max -= 32              # Parent
    payload_size_max -= 4               # PayloadLength
                                        # Placeholder for Payload
    payload_size_max -= 8               # Nonce
    
    return payload_size_max

#===============================================================================
# returns the maximum possible size of an output
def getOutputSizeMax(transaction_size_max, inputs=1):
    output_size_max = transaction_size_max
    output_size_max -= 4                # Payload Type
    output_size_max -= 1                # Transaction Type
    output_size_max -= 8                # NetworkID
    output_size_max -= 2                # Inputs Count
    for i in range(inputs):
        output_size_max -= (1+32+2)     # 1x UTXO Input (Input Type + Transaction ID + Transaction Output Index)
    output_size_max -= 32               # Inputs Commitment
    output_size_max -= 2                # Outputs Count
                                        # Placeholder for Outputs
    output_size_max -= 4                # Payload Length
                                        # Placeholder for Payload
    output_size_max -= 2                # Unlock Blocks Count
    for i in range(inputs):
        output_size_max -= (1+1+32+64)  # 1x Unlock Blocks (Unlock Type - Signature Type + Public key + Signature)    
    
    return output_size_max

#===============================================================================
class Output_VBytes(object):
    #---------------------------------------------------------------------------
    def __init__(self, name, name_plot, max_byte_size, weight_key, weight_data, metadata_length_max, plot_row_index=0, plot_column_index=0):
        self.name                   = name
        self.name_plot              = name_plot
        self.max_byte_size          = max_byte_size     # maximum available bytes
        self.weight_key             = weight_key
        self.weight_data            = weight_data
        self.metadata_length_max    = metadata_length_max

        self.plot_row_index         = plot_row_index
        self.plot_column_index      = plot_column_index 
        
        self.byte_size_max          = 0                 # currently used bytes max
        self.v_bytes_min            = 0
        self.v_bytes_max            = 0 

        self.plot_y_values          = []

    #---------------------------------------------------------------------------
    def summary(self):
        print("\nName: %s\n\tbytes_max:  %6d\n\tv_byte_min: %6d\n\tv_byte_max: %6d" % (self.name, self.byte_size_max, self.v_bytes_min, self.v_bytes_max))
    
    #---------------------------------------------------------------------------
    def addField(self, field_byte_size_min, field_byte_size_max, weight):
        self.byte_size_max   += field_byte_size_max
        if self.byte_size_max > self.max_byte_size:
            raise Exception("Output too big: %s, Current: %d, Max: %d" % (self.name, self.byte_size_max, self.max_byte_size))
        self.v_bytes_min += field_byte_size_min*weight 
        self.v_bytes_max += field_byte_size_max*weight 

    #---------------------------------------------------------------------------
    def byteSizeMax(self):
        return self.byte_size_max

    #---------------------------------------------------------------------------
    def bytesRemaining(self):
        return self.max_byte_size - self.byte_size_max

    #---------------------------------------------------------------------------
    def vBytesMin(self):
        return self.v_bytes_min

    #---------------------------------------------------------------------------
    def vBytesMax(self):
        return self.v_bytes_max

    #---------------------------------------------------------------------------
    def totalOutputsPossible(self, db_size_bytes_max):
        return int(db_size_bytes_max / self.byte_size_max)

    #################
    # Output Fields #
    #################

    #---------------------------------------------------------------------------
    def addField_OutputID(self):
        self.addField(field_byte_size_min=32+2, field_byte_size_max=32+2, weight=self.weight_key)               # Output ID (Transaction ID + Transaction Output Index)
    
    #---------------------------------------------------------------------------
    def addField_OutputMetadataOffsets(self):
        self.addField(field_byte_size_min=32,   field_byte_size_max=32, weight=self.weight_data)               # BlockID Included
        self.addField(field_byte_size_min=4,    field_byte_size_max=4,  weight=self.weight_data)               # Confirmation Milestone Index
        self.addField(field_byte_size_min=4,    field_byte_size_max=4,  weight=self.weight_data)               # Confirmation Unix Timestamp
    
    #---------------------------------------------------------------------------
    def addField_OutputType(self):
        self.addField(field_byte_size_min=1,   field_byte_size_max=1,  weight=self.weight_data)                 # Output Type

    #---------------------------------------------------------------------------
    def addField_IotaAmount(self):
        self.addField(field_byte_size_min=8,   field_byte_size_max=8,  weight=self.weight_data)                 # Amount

    #---------------------------------------------------------------------------
    def addField_NativeTokens(self, native_token_count):
        self.addField(field_byte_size_min=1,   field_byte_size_max=1,  weight=self.weight_data)                 # Native Tokens Count
        for i in range(native_token_count):
            self.addField(field_byte_size_min=38+32,  field_byte_size_max=38+32, weight=self.weight_data)       # Native Tokens (TokenID+Amount)

    #---------------------------------------------------------------------------
    def addField_AliasID(self):
        self.addField(field_byte_size_min=32,  field_byte_size_max=32, weight=self.weight_data)                 # Alias ID

    #---------------------------------------------------------------------------
    def addField_NFTID(self):
        self.addField(field_byte_size_min=32,  field_byte_size_max=32, weight=self.weight_data)                 # NFT ID

    #---------------------------------------------------------------------------
    def addField_StateIndex(self):
        self.addField(field_byte_size_min=4,   field_byte_size_max=4,  weight=self.weight_data)                 # State Index
    
    #---------------------------------------------------------------------------
    def addField_StateMetadata(self, max_data_length):
        self.addField(field_byte_size_min=2,   field_byte_size_max=2,  weight=self.weight_data)                 # State Metadata Length
        
        if max_data_length == None:
            max_data_length = 0
        
        if (self.metadata_length_max != None) and (max_data_length > self.metadata_length_max):
            max_data_length = self.metadata_length_max
        
        self.addField(field_byte_size_min=0,   field_byte_size_max=max_data_length,  weight=self.weight_data)   # State Metadata
    
    #---------------------------------------------------------------------------
    def addField_FoundryCounter(self):
        self.addField(field_byte_size_min=4,   field_byte_size_max=4,  weight=self.weight_data)                 # Foundry Counter

    #---------------------------------------------------------------------------
    def addField_SerialNumber(self):
        self.addField(field_byte_size_min=4,   field_byte_size_max=4,  weight=self.weight_data)                 # Serial Number

    #---------------------------------------------------------------------------
    def addField_TokenScheme(self):
        self.addField(field_byte_size_min=1,   field_byte_size_max=1,  weight=self.weight_data)                 # Token Scheme

    #---------------------------------------------------------------------------
    def addField_MintedTokens(self):
        self.addField(field_byte_size_min=32,  field_byte_size_max=32, weight=self.weight_data)                 # Minted Tokens

    #---------------------------------------------------------------------------
    def addField_MeltedTokens(self):
        self.addField(field_byte_size_min=32,  field_byte_size_max=32, weight=self.weight_data)                 # Melted Tokens

    #---------------------------------------------------------------------------
    def addField_MaximumSupply(self):
        self.addField(field_byte_size_min=32,  field_byte_size_max=32, weight=self.weight_data)                 # Maximum Supply

    #---------------------------------------------------------------------------
    def addField_UnlockConditionsCount(self):
        self.addField(field_byte_size_min=1,   field_byte_size_max=1,  weight=self.weight_data)                 # Unlock Conditions Count

    #---------------------------------------------------------------------------
    def addField_AddressUnlockCondition(self):
        self.addField(field_byte_size_min=1,   field_byte_size_max=1,  weight=self.weight_data)                 # Unlock Condition Type
        self.addField(field_byte_size_min=1,   field_byte_size_max=1,  weight=self.weight_data)                 # Address Type
        self.addField(field_byte_size_min=32,  field_byte_size_max=32, weight=self.weight_data)                 # Address (Alias Address, NFT Address, Ed25519 Address)
    
    #---------------------------------------------------------------------------
    def addField_StateControllerAddressUnlockCondition(self):
        self.addField(field_byte_size_min=1,   field_byte_size_max=1,  weight=self.weight_data)                 # Unlock Condition Type
        self.addField(field_byte_size_min=1,   field_byte_size_max=1,  weight=self.weight_data)                 # Address Type
        self.addField(field_byte_size_min=32,  field_byte_size_max=32, weight=self.weight_data)                 # Address (Alias Address, NFT Address, Ed25519 Address)
    
    #---------------------------------------------------------------------------
    def addField_GovernorAddressUnlockCondition(self):
        self.addField(field_byte_size_min=1,   field_byte_size_max=1,  weight=self.weight_data)                 # Unlock Condition Type
        self.addField(field_byte_size_min=1,   field_byte_size_max=1,  weight=self.weight_data)                 # Address Type
        self.addField(field_byte_size_min=32,  field_byte_size_max=32, weight=self.weight_data)                 # Address (Alias Address, NFT Address, Ed25519 Address)
    
    #---------------------------------------------------------------------------
    def addField_StorageDepositReturnUnlockCondition(self):
        self.addField(field_byte_size_min=1,   field_byte_size_max=1,  weight=self.weight_data)                 # Unlock Condition Type
        self.addField(field_byte_size_min=1,   field_byte_size_max=1,  weight=self.weight_data)                 # Return Address Type
        self.addField(field_byte_size_min=32,  field_byte_size_max=32, weight=self.weight_data)                 # Return Address (Alias Address, NFT Address, Ed25519 Address)
        self.addField(field_byte_size_min=8,   field_byte_size_max=8,  weight=self.weight_data)                 # Return Amount

    #---------------------------------------------------------------------------
    def addField_TimelockUnlockCondition(self):
        self.addField(field_byte_size_min=1,   field_byte_size_max=1,  weight=self.weight_data)                 # Unlock Condition Type
        self.addField(field_byte_size_min=4,   field_byte_size_max=4,  weight=self.weight_data)                 # Unix Time

    #---------------------------------------------------------------------------
    def addField_ExpirationUnlockCondition(self):
        self.addField(field_byte_size_min=1,   field_byte_size_max=1,  weight=self.weight_data)                 # Unlock Condition Type
        self.addField(field_byte_size_min=1,   field_byte_size_max=1,  weight=self.weight_data)                 # Address Type
        self.addField(field_byte_size_min=32,  field_byte_size_max=32, weight=self.weight_data)                 # Address (Alias Address, NFT Address, Ed25519 Address)
        self.addField(field_byte_size_min=4,   field_byte_size_max=4,  weight=self.weight_data)                 # Unix Time

    #---------------------------------------------------------------------------
    def addField_FeaturesCount(self):
        self.addField(field_byte_size_min=1,   field_byte_size_max=1,  weight=self.weight_data)                 # Features Count
    
    #---------------------------------------------------------------------------
    def addField_SenderFeature(self):
        self.addField(field_byte_size_min=1,   field_byte_size_max=1,  weight=self.weight_data)                 # Feature Type
        self.addField(field_byte_size_min=1,   field_byte_size_max=1,  weight=self.weight_data)                 # Address Type
        self.addField(field_byte_size_min=32,  field_byte_size_max=32, weight=self.weight_data)                 # Address (Alias Address, NFT Address, Ed25519 Address)

    #---------------------------------------------------------------------------
    def addField_MetadataFeature(self, max_data_length):
        self.addField(field_byte_size_min=1,   field_byte_size_max=1,  weight=self.weight_data)                 # Feature Type
        self.addField(field_byte_size_min=2,   field_byte_size_max=2,  weight=self.weight_data)                 # Metadata Data Length
        
        if max_data_length == None:
            max_data_length = 0
        
        if (self.metadata_length_max != None) and (max_data_length > self.metadata_length_max):
            max_data_length = self.metadata_length_max
        
        self.addField(field_byte_size_min=1,   field_byte_size_max=max_data_length, weight=self.weight_data)    # Metadata Data 

    #---------------------------------------------------------------------------
    def addField_TagFeature(self):
        self.addField(field_byte_size_min=1,   field_byte_size_max=1,  weight=self.weight_data)                 # Feature Type
        self.addField(field_byte_size_min=1,   field_byte_size_max=1,  weight=self.weight_data)                 # Tag Length
        self.addField(field_byte_size_min=1,   field_byte_size_max=255, weight=self.weight_data)                # Tag

    #---------------------------------------------------------------------------
    def addField_ImmutableFeaturesCount(self):
        self.addField(field_byte_size_min=1,   field_byte_size_max=1,  weight=self.weight_data)                 # Immutable Features Count

    #---------------------------------------------------------------------------
    def addField_ImmutableIssuerFeature(self):
        self.addField(field_byte_size_min=1,   field_byte_size_max=1,  weight=self.weight_data)                 # Immutable Feature Type
        self.addField(field_byte_size_min=1,   field_byte_size_max=1,  weight=self.weight_data)                 # Address Type
        self.addField(field_byte_size_min=32,  field_byte_size_max=32, weight=self.weight_data)                 # Address (Alias Address, NFT Address, Ed25519 Address)

    #---------------------------------------------------------------------------
    def addField_ImmutableMetadataFeature(self, max_data_length):
        self.addField(field_byte_size_min=1,   field_byte_size_max=1,  weight=self.weight_data)                 # Immutable Feature Type
        self.addField(field_byte_size_min=2,   field_byte_size_max=2,  weight=self.weight_data)                 # Immutable Metadata Length
        
        if max_data_length == None:
            max_data_length = 0
        
        if (self.metadata_length_max != None) and (max_data_length > self.metadata_length_max):
            max_data_length = self.metadata_length_max

        self.addField(field_byte_size_min=1,   field_byte_size_max=max_data_length,  weight=self.weight_data)   # Immutable Metadata
    
#===============================================================================
def getVBytes_SingleByte():

    vbytes = Output_VBytes(name="byte", name_plot="byte", max_byte_size=1, weight_key=1.0, weight_data=1.0)
    vbytes.addField(field_byte_size_min=1,  field_byte_size_max=1, weight=1.0)
    
    return vbytes

#===============================================================================
def getVBytes_SigLockedSingleOutput(weight_key,
                                    weight_data,
                                    additional_name,
                                    output_size_max,
                                   ):

    name        = "SigLockedSingleOutput"
    name_plot   = name
    if additional_name != None:
        name        = "%s (%s)" %  (name, additional_name)
        name_plot   = "%s\n(%s)" % (name_plot, additional_name)
    
    vbytes = Output_VBytes(name                = name,
                           name_plot           = name_plot,
                           max_byte_size       = output_size_max,
                           weight_key          = weight_key,
                           weight_data         = weight_data,
                           metadata_length_max = None)

    vbytes.addField_OutputID()
    vbytes.addField_OutputType()
    vbytes.addField(field_byte_size_min=1,   field_byte_size_max=1,  weight=weight_data)                 # Address Type
    vbytes.addField(field_byte_size_min=32,  field_byte_size_max=32, weight=weight_data)                 # Address (Ed25519 Address)
    vbytes.addField_IotaAmount()

    return vbytes

#===============================================================================
def getVBytes_BasicOutput(weight_key,
                          weight_data,
                          additional_name,
                          output_size_max,
                          metadata_length_max,
                          native_token_count, 
                          storage_deposit_return_unlock_condition,
                          timelock_unlock_condition,
                          expiration_unlock_condition,
                          sender_feature,
                          metadata_feature,
                          metadata_length,
                          tag_feature,
                         ):

    name        = "BasicOutput"
    name_plot   = name
    if additional_name != None:
        name        = "%s (%s)" %  (name, additional_name)
        name_plot   = "%s\n(%s)" % (name_plot, additional_name)
    
    vbytes = Output_VBytes(name                = name,
                           name_plot           = name_plot,
                           max_byte_size       = output_size_max,
                           weight_key          = weight_key,
                           weight_data         = weight_data,
                           metadata_length_max = metadata_length_max)

    vbytes.addField_OutputID()
    vbytes.addField_OutputMetadataOffsets()

    vbytes.addField_OutputType()
    vbytes.addField_IotaAmount()
    vbytes.addField_NativeTokens(native_token_count)
    
    # Unlock conditions
    vbytes.addField_UnlockConditionsCount()
    vbytes.addField_AddressUnlockCondition()
    
    if storage_deposit_return_unlock_condition:
        vbytes.addField_StorageDepositReturnUnlockCondition()

    if timelock_unlock_condition:
        vbytes.addField_TimelockUnlockCondition()
    
    if expiration_unlock_condition:
        vbytes.addField_ExpirationUnlockCondition()
    
    # Feature blocks
    vbytes.addField_FeaturesCount()
    
    if sender_feature:
        vbytes.addField_SenderFeature()

    if metadata_feature:
        vbytes.addField_MetadataFeature(max_data_length=metadata_length)
    
    if tag_feature:
        vbytes.addField_TagFeature()
    
    return vbytes

#===============================================================================
def getVBytes_AliasOutput(weight_key,
                          weight_data,
                          additional_name,
                          output_size_max,
                          metadata_length_max,
                          native_token_count, 
                          state_metadata_length,
                          governor_address_unlock_condition,
                          sender_feature,
                          metadata_feature,
                          metadata_length,
                          immutable_issuer_feature,
                          immutable_metadata_feature,
                          immutable_metadata_length,
                         ):

    name        = "AliasOutput"
    name_plot   = name
    if additional_name != None:
        name        = "%s (%s)" %  (name, additional_name)
        name_plot   = "%s\n(%s)" % (name_plot, additional_name)
    
    vbytes = Output_VBytes(name                = name,
                           name_plot           = name_plot,
                           max_byte_size       = output_size_max,
                           weight_key          = weight_key,
                           weight_data         = weight_data,
                           metadata_length_max = metadata_length_max)

    vbytes.addField_OutputID()
    vbytes.addField_OutputMetadataOffsets()

    vbytes.addField_OutputType()
    vbytes.addField_IotaAmount()
    vbytes.addField_NativeTokens(native_token_count)    
    vbytes.addField_AliasID()
    vbytes.addField_StateIndex()
    vbytes.addField_StateMetadata(max_data_length=state_metadata_length)
    vbytes.addField_FoundryCounter()

    # Unlock conditions
    vbytes.addField_UnlockConditionsCount()
    vbytes.addField_StateControllerAddressUnlockCondition()
    
    if governor_address_unlock_condition:
        vbytes.addField_GovernorAddressUnlockCondition()
    
    # Feature blocks
    vbytes.addField_FeaturesCount()
    
    if sender_feature:
        vbytes.addField_SenderFeature()

    if metadata_feature:
        vbytes.addField_MetadataFeature(max_data_length=metadata_length)
    
    # Immutable blocks
    vbytes.addField_ImmutableFeaturesCount()
    
    if immutable_issuer_feature:
        vbytes.addField_ImmutableIssuerFeature()
    
    if immutable_metadata_feature:
        vbytes.addField_ImmutableMetadataFeature(max_data_length=immutable_metadata_length)
    
    return vbytes

#===============================================================================
def getVBytes_FoundryOutput(weight_key,
                            weight_data,
                            additional_name,
                            output_size_max,
                            metadata_length_max,
                            native_token_count, 
                            metadata_feature,
                            metadata_length,
                            immutable_metadata_feature,
                            immutable_metadata_length,
                           ):

    name        = "FoundryOutput"
    name_plot   = name
    if additional_name != None:
        name        = "%s (%s)" %  (name, additional_name)
        name_plot   = "%s\n(%s)" % (name_plot, additional_name)
    
    vbytes = Output_VBytes(name                = name,
                           name_plot           = name_plot,
                           max_byte_size       = output_size_max,
                           weight_key          = weight_key,
                           weight_data         = weight_data,
                           metadata_length_max = metadata_length_max)

    vbytes.addField_OutputID()
    vbytes.addField_OutputMetadataOffsets()

    vbytes.addField_OutputType()
    vbytes.addField_IotaAmount()
    vbytes.addField_NativeTokens(native_token_count)    
    vbytes.addField_SerialNumber()
    vbytes.addField_TokenScheme()
    vbytes.addField_MintedTokens()
    vbytes.addField_MeltedTokens()
    vbytes.addField_MaximumSupply()

    # Unlock conditions
    vbytes.addField_UnlockConditionsCount()
    vbytes.addField_AddressUnlockCondition()

    # Feature blocks
    vbytes.addField_FeaturesCount()
    
    if metadata_feature:
        vbytes.addField_MetadataFeature(max_data_length=metadata_length)
    
    # Immutable blocks
    vbytes.addField_ImmutableFeaturesCount()
    
    if immutable_metadata_feature:
        vbytes.addField_ImmutableMetadataFeature(max_data_length=immutable_metadata_length)
    
    return vbytes

#===============================================================================
def getVBytes_NFTOutput(weight_key,
                        weight_data,
                        additional_name,
                        output_size_max,
                        metadata_length_max,
                        native_token_count,
                        storage_deposit_return_unlock_condition,
                        timelock_unlock_condition,
                        expiration_unlock_condition,
                        sender_feature,
                        metadata_feature,
                        metadata_length,
                        tag_feature,
                        immutable_issuer_feature,
                        immutable_metadata_feature,
                        immutable_metadata_length):

    name        = "NFTOutput"
    name_plot   = name
    if additional_name != None:
        name        = "%s (%s)" %  (name, additional_name)
        name_plot   = "%s\n(%s)" % (name_plot, additional_name)
    
    vbytes = Output_VBytes(name                = name,
                           name_plot           = name_plot,
                           max_byte_size       = output_size_max,
                           weight_key          = weight_key,
                           weight_data         = weight_data,
                           metadata_length_max = metadata_length_max)

    vbytes.addField_OutputID()
    vbytes.addField_OutputMetadataOffsets()

    vbytes.addField_OutputType()
    vbytes.addField_IotaAmount()
    vbytes.addField_NativeTokens(native_token_count)    
    vbytes.addField_NFTID()
    
    # Unlock conditions
    vbytes.addField_UnlockConditionsCount()
    vbytes.addField_AddressUnlockCondition()
    
    if storage_deposit_return_unlock_condition:
        vbytes.addField_StorageDepositReturnUnlockCondition()

    if timelock_unlock_condition:
        vbytes.addField_TimelockUnlockCondition()
    
    if expiration_unlock_condition:
        vbytes.addField_ExpirationUnlockCondition()
        
    # Feature blocks
    vbytes.addField_FeaturesCount()
    
    if sender_feature:
        vbytes.addField_SenderFeature()

    if metadata_feature:
        vbytes.addField_MetadataFeature(max_data_length=metadata_length)
    
    if tag_feature:
        vbytes.addField_TagFeature()
    
    # Immutable blocks
    vbytes.addField_ImmutableFeaturesCount()
    
    if immutable_issuer_feature:
        vbytes.addField_ImmutableIssuerFeature()
    
    if immutable_metadata_feature:
        vbytes.addField_ImmutableMetadataFeature(max_data_length=immutable_metadata_length)
    
    return vbytes

#===============================================================================
def GetExampleOutputs(output_size_max,
                      native_token_count_max,
                      weight_key,
                      weight_data,
                      metadata_length_max,
                     ):

    return [getVBytes_SigLockedSingleOutput(
                weight_key                              = weight_key,
                weight_data                             = weight_data,
                additional_name                         = None,
                output_size_max                         = output_size_max,
            ), 
            getVBytes_BasicOutput(
                weight_key                              = weight_key,
                weight_data                             = weight_data,
                additional_name                         = "min functionality",
                output_size_max                         = output_size_max,
                metadata_length_max                     = metadata_length_max,
                native_token_count                      = 0,
                storage_deposit_return_unlock_condition = False,
                timelock_unlock_condition               = False,
                expiration_unlock_condition             = False,
                sender_feature                          = False,
                metadata_feature                        = False,
                metadata_length                         = 0,
                tag_feature                             = False,
            ),
            getVBytes_BasicOutput(
                weight_key                              = weight_key,
                weight_data                             = weight_data,
                additional_name                         = "max functionality",
                output_size_max                         = output_size_max,
                metadata_length_max                     = metadata_length_max,
                native_token_count                      = native_token_count_max,
                storage_deposit_return_unlock_condition = True,
                timelock_unlock_condition               = True,
                expiration_unlock_condition             = True,
                sender_feature                          = True,
                metadata_feature                        = True,
                metadata_length                         = metadata_length_max,
                tag_feature                             = True,
            ),
            getVBytes_BasicOutput(
                weight_key                              = weight_key,
                weight_data                             = weight_data,
                additional_name                         = "1000 byte metadata",
                output_size_max                         = output_size_max,
                metadata_length_max                     = metadata_length_max,
                native_token_count                      = 0,
                storage_deposit_return_unlock_condition = False,
                timelock_unlock_condition               = False,
                expiration_unlock_condition             = False,
                sender_feature                          = False,
                metadata_feature                        = True,
                metadata_length                         = 1000,
                tag_feature                             = False,
            ),
            getVBytes_BasicOutput(
                weight_key                              = weight_key,
                weight_data                             = weight_data,
                additional_name                         = "1 native token, storage deposit return, expiration",
                output_size_max                         = output_size_max,
                metadata_length_max                     = metadata_length_max,
                native_token_count                      = 1,
                storage_deposit_return_unlock_condition = True,
                timelock_unlock_condition               = False,
                expiration_unlock_condition             = True,
                sender_feature                          = False,
                metadata_feature                        = False,
                metadata_length                         = 0,
                tag_feature                             = False,
            ),
            getVBytes_BasicOutput(
                weight_key                              = weight_key,
                weight_data                             = weight_data,
                additional_name                         = "typical ISC request",
                output_size_max                         = output_size_max,
                metadata_length_max                     = metadata_length_max,
                native_token_count                      = 0,
                storage_deposit_return_unlock_condition = True,
                timelock_unlock_condition               = False,
                expiration_unlock_condition             = True,
                sender_feature                          = True,
                metadata_feature                        = True,
                metadata_length                         = 64,
                tag_feature                             = False,
            ),
            getVBytes_AliasOutput(
                weight_key                              = weight_key,
                weight_data                             = weight_data,
                additional_name                         = "min functionality",
                output_size_max                         = output_size_max,
                metadata_length_max                     = metadata_length_max,
                native_token_count                      = 0,
                state_metadata_length                   = 0,
                governor_address_unlock_condition       = False,
                sender_feature                          = False,
                metadata_feature                        = False,
                metadata_length                         = 0,
                immutable_issuer_feature                = False,
                immutable_metadata_feature              = False,
                immutable_metadata_length               = 0,
            ),
            getVBytes_AliasOutput(
                weight_key                              = weight_key,
                weight_data                             = weight_data,
                additional_name                         = "max functionality",
                output_size_max                         = output_size_max,
                metadata_length_max                     = metadata_length_max,
                native_token_count                      = native_token_count_max,
                state_metadata_length                   = metadata_length_max,
                governor_address_unlock_condition       = True,
                sender_feature                          = True,
                metadata_feature                        = True,
                metadata_length                         = metadata_length_max,
                immutable_issuer_feature                = True,
                immutable_metadata_feature              = True,
                immutable_metadata_length               = metadata_length_max,
            ),
            getVBytes_FoundryOutput(
                weight_key                              = weight_key,
                weight_data                             = weight_data,
                additional_name                         = "min functionality",
                output_size_max                         = output_size_max,
                metadata_length_max                     = metadata_length_max,
                native_token_count                      = 0,
                metadata_feature                        = False,
                metadata_length                         = 0,
                immutable_metadata_feature              = False,
                immutable_metadata_length               = 0,
            ),
            getVBytes_FoundryOutput(
                weight_key                              = weight_key,
                weight_data                             = weight_data,
                additional_name                         = "max functionality",
                output_size_max                         = output_size_max,
                metadata_length_max                     = metadata_length_max,
                native_token_count                      = native_token_count_max,
                metadata_feature                        = True,
                metadata_length                         = metadata_length_max,
                immutable_metadata_feature              = True,
                immutable_metadata_length               = metadata_length_max,
            ),
            getVBytes_NFTOutput(
                weight_key                              = weight_key,
                weight_data                             = weight_data,
                additional_name                         = "min functionality",
                output_size_max                         = output_size_max,
                metadata_length_max                     = metadata_length_max,
                native_token_count                      = 0,
                storage_deposit_return_unlock_condition = False,
                timelock_unlock_condition               = False,
                expiration_unlock_condition             = False,
                sender_feature                          = False,
                metadata_feature                        = False,
                metadata_length                         = 0,
                tag_feature                             = False,
                immutable_issuer_feature                = False,
                immutable_metadata_feature              = False,
                immutable_metadata_length               = 0,
            ),
            getVBytes_NFTOutput(
                weight_key                              = weight_key,
                weight_data                             = weight_data,
                additional_name                         = "max functionality",
                output_size_max                         = output_size_max,
                metadata_length_max                     = metadata_length_max,
                native_token_count                      = native_token_count_max,
                storage_deposit_return_unlock_condition = True,
                timelock_unlock_condition               = True,
                expiration_unlock_condition             = True,
                sender_feature                          = True,
                metadata_feature                        = True,
                metadata_length                         = metadata_length_max,
                tag_feature                             = True,
                immutable_issuer_feature                = True,
                immutable_metadata_feature              = True,
                immutable_metadata_length               = metadata_length_max,
            ),
            getVBytes_NFTOutput(
                weight_key                              = weight_key,
                weight_data                             = weight_data,
                additional_name                         = "typical NFT",
                output_size_max                         = output_size_max,
                metadata_length_max                     = metadata_length_max,
                native_token_count                      = 0,
                storage_deposit_return_unlock_condition = False,
                timelock_unlock_condition               = False,
                expiration_unlock_condition             = False,
                sender_feature                          = False,
                metadata_feature                        = False,
                metadata_length                         = 0,
                tag_feature                             = False,
                immutable_issuer_feature                = True,
                immutable_metadata_feature              = True,
                immutable_metadata_length               = len('''{
  "standard" : "IRC27",
  "type": "image",
  "version": "v1.0",
  "nftId": "vt7rye8tgvr7e89w",
  "tokenURI": "https://mywebsite.com/myfile.png",
  "tokenName": "My NFT #0001",
  "collectionId": "7f9e0rwf7e90w",
  "collectionName": "My Collection of Art",
  "royalties": {
    "atoi1qptd4dlt2870zsa9fn5t98mnt2zsstlert0wd20uesk0h4thzavmgrld8kk": 0.025,
    "atoi1qptd4dlt2870zsa9fn5t98mnt2zsstlert0wd20uesk0h4thzavmgrld8kk": 0.025
  },
  "issuerName": "My Artist Name",
  "description": "A little information about my NFT collection",
  "attributes": {
    "Background": "Purple",
    "Element": "Water",
    "Attack": "150",
    "Health": "500"
  }
}'''),
            ),            
    ]

#===============================================================================
if __name__ == '__main__':
    BLOCK_SIZE_MAX          = 32768
    METADATA_LENGTH_MAX     = 8192
    NATIVE_TOKEN_COUNT_MAX  = 64

    WEIGHT_KEY              = 10.0
    WEIGHT_DATA             = 1.0

    payload_size_max        = getPayloadSizeMax(block_size_max=BLOCK_SIZE_MAX)
    output_size_max         = getOutputSizeMax(transaction_size_max=payload_size_max, inputs=1)
    
    print("BlockSizeMax:        %5d" % (BLOCK_SIZE_MAX))
    print("PayloadSizeMax:      %5d" % (payload_size_max))
    print("OutputSizeMax:       %5d" % (output_size_max))
    print("MetadataLengthMax:   %5d" % (METADATA_LENGTH_MAX))
    print("NativeTokenCountMax: %5d" % (NATIVE_TOKEN_COUNT_MAX))

    for vbytes in GetExampleOutputs(output_size_max         = output_size_max,
                                    native_token_count_max  = NATIVE_TOKEN_COUNT_MAX,
                                    weight_key              = WEIGHT_KEY,
                                    weight_data             = WEIGHT_DATA,
                                    metadata_length_max     = METADATA_LENGTH_MAX,
                                   ):
        vbytes.summary()
