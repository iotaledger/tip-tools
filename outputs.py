# -*- coding: utf-8 -*-

#===============================================================================
# returns the maximum possible size of a payload
def getPayloadSizeMax(message_size_max):
    payload_size_max = message_size_max
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
        self.addField(field_byte_size_min=32,   field_byte_size_max=32, weight=self.weight_data)               # MessageID Included
        self.addField(field_byte_size_min=4,    field_byte_size_max=4,  weight=self.weight_data)               # Milestone Index Booked
        self.addField(field_byte_size_min=4,    field_byte_size_max=4,  weight=self.weight_data)               # Milestone Timestamp Booked
    
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
        self.addField(field_byte_size_min=20,  field_byte_size_max=20, weight=self.weight_data)                 # Alias ID

    #---------------------------------------------------------------------------
    def addField_NFTID(self):
        self.addField(field_byte_size_min=20,  field_byte_size_max=20, weight=self.weight_data)                 # NFT ID

    #---------------------------------------------------------------------------
    def addField_StateIndex(self):
        self.addField(field_byte_size_min=4,   field_byte_size_max=4,  weight=self.weight_data)                 # State Index
    
    #---------------------------------------------------------------------------
    def addField_StateMetadata(self, max_data_length):
        self.addField(field_byte_size_min=2,   field_byte_size_max=2,  weight=self.weight_data)                 # State Metadata Length
        
        if max_data_length == None:
            max_data_length = 0       # zero for now, the remaining space will be taken into account in the metadata block
        
        if (self.metadata_length_max != None) and (max_data_length > self.metadata_length_max):
            max_data_length = self.metadata_length_max
        
        self.addField(field_byte_size_min=0,   field_byte_size_max=max_data_length,  weight=self.weight_data)
    
    #---------------------------------------------------------------------------
    def addField_ImmutableMetadata(self, max_data_length):
        self.addField(field_byte_size_min=2,   field_byte_size_max=2,  weight=self.weight_data)                 # Immutable Metadata Length
        
        if max_data_length == None:
            max_data_length = 0       # zero for now, the remaining space will be taken into account in the metadata block
        
        if (self.metadata_length_max != None) and (max_data_length > self.metadata_length_max):
            max_data_length = self.metadata_length_max

        self.addField(field_byte_size_min=0,   field_byte_size_max=max_data_length,  weight=self.weight_data)   # Immutable Metadata
    
    #---------------------------------------------------------------------------
    def addField_MetadataBlock(self, max_data_length):
        self.addField(field_byte_size_min=1,   field_byte_size_max=1,  weight=self.weight_data)                 # Block Type
        self.addField(field_byte_size_min=2,   field_byte_size_max=2,  weight=self.weight_data)                 # Metadata Data Length
        
        if max_data_length == None:
            max_data_length = self.bytesRemaining()       # we can just use the remaining size here since every other dynamic field has the same weight
        
        if (self.metadata_length_max != None) and (max_data_length > self.metadata_length_max):
            max_data_length = self.metadata_length_max
        
        self.addField(field_byte_size_min=1,   field_byte_size_max=max_data_length, weight=self.weight_data)    # Metadata Data 

    #---------------------------------------------------------------------------
    def addField_FoundryCounter(self):
        self.addField(field_byte_size_min=4,   field_byte_size_max=4,  weight=self.weight_data)                 # Foundry Counter

    #---------------------------------------------------------------------------
    def addField_SerialNumber(self):
        self.addField(field_byte_size_min=4,   field_byte_size_max=4,  weight=self.weight_data)                 # Serial Number

    #---------------------------------------------------------------------------
    def addField_TokenTag(self):
        self.addField(field_byte_size_min=12,  field_byte_size_max=12, weight=self.weight_data)                 # Token Tag

    #---------------------------------------------------------------------------
    def addField_CirculatingSupply(self):
        self.addField(field_byte_size_min=32,  field_byte_size_max=32, weight=self.weight_data)                 # Circulating Supply

    #---------------------------------------------------------------------------
    def addField_MaximumSupply(self):
        self.addField(field_byte_size_min=32,  field_byte_size_max=32, weight=self.weight_data)                 # Maximum Supply

    #---------------------------------------------------------------------------
    def addField_TokenScheme(self):
        self.addField(field_byte_size_min=1,   field_byte_size_max=1,  weight=self.weight_data)                 # Token Scheme
        
    #---------------------------------------------------------------------------
    def addField_UnlockConditionsCount(self):
        self.addField(field_byte_size_min=1,   field_byte_size_max=1,  weight=self.weight_data)                 # Unlock Conditions Count

    #---------------------------------------------------------------------------
    def addField_AddressUnlockCondition(self):
        self.addField(field_byte_size_min=1,   field_byte_size_max=1,  weight=self.weight_data)                 # Unlock Condition Type
        self.addField(field_byte_size_min=1,   field_byte_size_max=1,  weight=self.weight_data)                 # Address Type
        self.addField(field_byte_size_min=20,  field_byte_size_max=32, weight=self.weight_data)                 # Address (Alias Address, NFT Address, Ed25519 Address)
    
    #---------------------------------------------------------------------------
    def addField_AddressUnlockCondition_AliasOnly(self):
        self.addField(field_byte_size_min=1,   field_byte_size_max=1,  weight=self.weight_data)                 # Unlock Condition Type
        self.addField(field_byte_size_min=1,   field_byte_size_max=1,  weight=self.weight_data)                 # Address Type
        self.addField(field_byte_size_min=20,  field_byte_size_max=20, weight=self.weight_data)                 # Address (Alias Address)
    
    #---------------------------------------------------------------------------
    def addField_StateControllerAddressUnlockCondition(self):
        self.addField(field_byte_size_min=1,   field_byte_size_max=1,  weight=self.weight_data)                 # Unlock Condition Type
        self.addField(field_byte_size_min=1,   field_byte_size_max=1,  weight=self.weight_data)                 # Address Type
        self.addField(field_byte_size_min=20,  field_byte_size_max=32, weight=self.weight_data)                 # Address (Alias Address, NFT Address, Ed25519 Address)
    
    #---------------------------------------------------------------------------
    def addField_GovernorAddressUnlockCondition(self):
        self.addField(field_byte_size_min=1,   field_byte_size_max=1,  weight=self.weight_data)                 # Unlock Condition Type
        self.addField(field_byte_size_min=1,   field_byte_size_max=1,  weight=self.weight_data)                 # Address Type
        self.addField(field_byte_size_min=20,  field_byte_size_max=32, weight=self.weight_data)                 # Address (Alias Address, NFT Address, Ed25519 Address)
    
    #---------------------------------------------------------------------------
    def addField_DustDepositReturnUnlockCondition(self):
        self.addField(field_byte_size_min=1,   field_byte_size_max=1,  weight=self.weight_data)                 # Unlock Condition Type
        self.addField(field_byte_size_min=1,   field_byte_size_max=1,  weight=self.weight_data)                 # Return Address Type
        self.addField(field_byte_size_min=20,  field_byte_size_max=32, weight=self.weight_data)                 # Return Address (Alias Address, NFT Address, Ed25519 Address)
        self.addField(field_byte_size_min=8,   field_byte_size_max=8,  weight=self.weight_data)                 # Return Amount

    #---------------------------------------------------------------------------
    def addField_TimelockUnlockCondition(self):
        self.addField(field_byte_size_min=1,   field_byte_size_max=1,  weight=self.weight_data)                 # Unlock Condition Type
        self.addField(field_byte_size_min=4,   field_byte_size_max=4,  weight=self.weight_data)                 # Milestone Index
        self.addField(field_byte_size_min=4,   field_byte_size_max=4,  weight=self.weight_data)                 # Unix Time

    #---------------------------------------------------------------------------
    def addField_ExpirationUnlockCondition(self):
        self.addField(field_byte_size_min=1,   field_byte_size_max=1,  weight=self.weight_data)                 # Unlock Condition Type
        self.addField(field_byte_size_min=1,   field_byte_size_max=1,  weight=self.weight_data)                 # Address Type
        self.addField(field_byte_size_min=20,  field_byte_size_max=32, weight=self.weight_data)                 # Address (Alias Address, NFT Address, Ed25519 Address)
        self.addField(field_byte_size_min=4,   field_byte_size_max=4,  weight=self.weight_data)                 # Milestone Index
        self.addField(field_byte_size_min=4,   field_byte_size_max=4,  weight=self.weight_data)                 # Unix Time

    #---------------------------------------------------------------------------
    def addField_FeatureBlocksCount(self):
        self.addField(field_byte_size_min=1,   field_byte_size_max=1,  weight=self.weight_data)                 # Blocks Count
    
    #---------------------------------------------------------------------------
    def addField_SenderBlock(self):
        self.addField(field_byte_size_min=1,   field_byte_size_max=1,  weight=self.weight_data)                 # Block Type
        self.addField(field_byte_size_min=1,   field_byte_size_max=1,  weight=self.weight_data)                 # Address Type
        self.addField(field_byte_size_min=20,  field_byte_size_max=32, weight=self.weight_data)                 # Address (Alias Address, NFT Address, Ed25519 Address)

    #---------------------------------------------------------------------------
    def addField_IssuerBlock(self):
        self.addField(field_byte_size_min=1,   field_byte_size_max=1,  weight=self.weight_data)                 # Block Type
        self.addField(field_byte_size_min=1,   field_byte_size_max=1,  weight=self.weight_data)                 # Address Type
        self.addField(field_byte_size_min=20,  field_byte_size_max=32, weight=self.weight_data)                 # Address (Alias Address, NFT Address, Ed25519 Address)

    #---------------------------------------------------------------------------
    def addField_TagBlock(self):
        self.addField(field_byte_size_min=1,   field_byte_size_max=1,  weight=self.weight_data)                 # Block Type
        self.addField(field_byte_size_min=1,   field_byte_size_max=1,  weight=self.weight_data)                 # Tag Length
        self.addField(field_byte_size_min=1,   field_byte_size_max=255, weight=self.weight_data)                # Tag

#===============================================================================
def getVBytes_SingleByte():

    vbytes = Output_VBytes(name="byte", name_plot="byte", max_byte_size=1, weight_key=1.0, weight_data=1.0)
    vbytes.addField(field_byte_size_min=1,  field_byte_size_max=1, weight=1.0)
    
    return vbytes

#===============================================================================
def getVBytes_SigLockedSingleOutput(weight_key,
                                    weight_data,
                                    additional_name,
                                    output_size_max):

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
                          dust_deposit_return_unlock_condition,
                          timelock_unlock_condition,
                          expiration_unlock_condition,
                          sender_block,
                          tag_block,
                          metadata_block,
                          metadata_length):

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
    
    if dust_deposit_return_unlock_condition:
        vbytes.addField_DustDepositReturnUnlockCondition()

    if timelock_unlock_condition:
        vbytes.addField_TimelockUnlockCondition()
    
    if expiration_unlock_condition:
        vbytes.addField_ExpirationUnlockCondition()
    
    # Feature blocks
    vbytes.addField_FeatureBlocksCount()
    
    if sender_block:
        vbytes.addField_SenderBlock()

    if tag_block:
        vbytes.addField_TagBlock()
    
    if metadata_block:
        vbytes.addField_MetadataBlock(max_data_length=metadata_length)
    
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
                          sender_block,
                          issuer_block,
                          metadata_block,
                          metadata_length):

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
    vbytes.addField_FeatureBlocksCount()
    
    if sender_block:
        vbytes.addField_SenderBlock()

    if issuer_block:
        vbytes.addField_IssuerBlock()
    
    if metadata_block:
        vbytes.addField_MetadataBlock(max_data_length=metadata_length)
    
    return vbytes

#===============================================================================
def getVBytes_FoundryOutput(weight_key,
                            weight_data,
                            additional_name,
                            output_size_max,
                            metadata_length_max,
                            native_token_count, 
                            metadata_block,
                            metadata_length):

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
    vbytes.addField_TokenTag()
    vbytes.addField_CirculatingSupply()
    vbytes.addField_MaximumSupply()
    vbytes.addField_TokenScheme()

    # Unlock conditions
    vbytes.addField_UnlockConditionsCount()
    vbytes.addField_AddressUnlockCondition_AliasOnly()

    # Feature blocks
    vbytes.addField_FeatureBlocksCount()
    
    if metadata_block:
        vbytes.addField_MetadataBlock(max_data_length=metadata_length)
    
    return vbytes

#===============================================================================
def getVBytes_NFTOutput(weight_key,
                        weight_data,
                        additional_name,
                        output_size_max,
                        metadata_length_max,
                        native_token_count,
                        immutable_metadata_length,
                        dust_deposit_return_unlock_condition,
                        timelock_unlock_condition,
                        expiration_unlock_condition,
                        sender_block,
                        issuer_block,
                        tag_block,
                        metadata_block,
                        metadata_length):

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
    vbytes.addField_ImmutableMetadata(max_data_length=immutable_metadata_length)
    
    # Unlock conditions
    vbytes.addField_UnlockConditionsCount()
    vbytes.addField_AddressUnlockCondition()
    
    if dust_deposit_return_unlock_condition:
        vbytes.addField_DustDepositReturnUnlockCondition()

    if timelock_unlock_condition:
        vbytes.addField_TimelockUnlockCondition()
    
    if expiration_unlock_condition:
        vbytes.addField_ExpirationUnlockCondition()
        
    # Feature blocks
    vbytes.addField_FeatureBlocksCount()
    
    if sender_block:
        vbytes.addField_SenderBlock()

    if issuer_block:
        vbytes.addField_IssuerBlock()
    
    if tag_block:
        vbytes.addField_TagBlock()
    
    if metadata_block:
        vbytes.addField_MetadataBlock(max_data_length=metadata_length)
    
    return vbytes

#===============================================================================
if __name__ == '__main__':
    MSG_SIZE_MAX            = 32768
    METADATA_LENGTH_MAX     = 8192
    NATIVE_TOKEN_COUNT_MAX  = 64

    WEIGHT_KEY              = 10.0
    WEIGHT_DATA             = 1.0

    payload_size_max        = getPayloadSizeMax(message_size_max=MSG_SIZE_MAX)
    output_size_max         = getOutputSizeMax(transaction_size_max=payload_size_max, inputs=1)
    
    print("MessageSizeMax:      %5d" % (MSG_SIZE_MAX))
    print("PayloadSizeMax:      %5d" % (payload_size_max))
    print("OutputSizeMax:       %5d" % (output_size_max))
    print("MetadataLengthMax:   %5d" % (METADATA_LENGTH_MAX))
    print("NativeTokenCountMax: %5d" % (NATIVE_TOKEN_COUNT_MAX))

    for vbytes in [getVBytes_SigLockedSingleOutput(
                        weight_key                              = WEIGHT_KEY,
                        weight_data                             = WEIGHT_DATA,
                        additional_name                         = None,
                        output_size_max                         = output_size_max,
                   ), 
                   getVBytes_BasicOutput(
                        weight_key                              = WEIGHT_KEY,
                        weight_data                             = WEIGHT_DATA,
                        additional_name                         = "min functionality",
                        output_size_max                         = output_size_max,
                        metadata_length_max                     = METADATA_LENGTH_MAX,
                        native_token_count                      = 0,
                        dust_deposit_return_unlock_condition    = False,
                        timelock_unlock_condition               = False,
                        expiration_unlock_condition             = False,
                        sender_block                            = False,
                        tag_block                               = False,
                        metadata_block                          = False,
                        metadata_length                         = 0,
                    ),
                   getVBytes_BasicOutput(
                        weight_key                              = WEIGHT_KEY,
                        weight_data                             = WEIGHT_DATA,
                        additional_name                         = "max functionality",
                        output_size_max                         = output_size_max,
                        metadata_length_max                     = METADATA_LENGTH_MAX,
                        native_token_count                      = NATIVE_TOKEN_COUNT_MAX,
                        dust_deposit_return_unlock_condition    = True,
                        timelock_unlock_condition               = True,
                        expiration_unlock_condition             = True,
                        sender_block                            = True,
                        tag_block                               = True,
                        metadata_block                          = True,
                        metadata_length                         = METADATA_LENGTH_MAX,
                   ),
                   getVBytes_AliasOutput(
                        weight_key                              = WEIGHT_KEY,
                        weight_data                             = WEIGHT_DATA,
                        additional_name                         = "min functionality",
                        output_size_max                         = output_size_max,
                        metadata_length_max                     = METADATA_LENGTH_MAX,
                        native_token_count                      = 0,
                        state_metadata_length                   = 0,
                        governor_address_unlock_condition       = False,
                        sender_block                            = False,
                        issuer_block                            = False,
                        metadata_block                          = False,
                        metadata_length                         = 0,
                   ),
                   getVBytes_AliasOutput(
                        weight_key                              = WEIGHT_KEY,
                        weight_data                             = WEIGHT_DATA,
                        additional_name                         = "max functionality",
                        output_size_max                         = output_size_max,
                        metadata_length_max                     = METADATA_LENGTH_MAX,
                        native_token_count                      = NATIVE_TOKEN_COUNT_MAX,
                        state_metadata_length                   = METADATA_LENGTH_MAX,
                        governor_address_unlock_condition       = True,
                        sender_block                            = True,
                        issuer_block                            = True,
                        metadata_block                          = True,
                        metadata_length                         = METADATA_LENGTH_MAX,
                   ),
                   getVBytes_FoundryOutput(
                        weight_key                              = WEIGHT_KEY,
                        weight_data                             = WEIGHT_DATA,
                        additional_name                         = "min functionality",
                        output_size_max                         = output_size_max,
                        metadata_length_max                     = METADATA_LENGTH_MAX,
                        native_token_count                      = 0,
                        metadata_block                          = False,
                        metadata_length                         = 0,
                   ),
                   getVBytes_FoundryOutput(
                        weight_key                              = WEIGHT_KEY,
                        weight_data                             = WEIGHT_DATA,
                        additional_name                         = "max functionality",
                        output_size_max                         = output_size_max,
                        metadata_length_max                     = METADATA_LENGTH_MAX,
                        native_token_count                      = NATIVE_TOKEN_COUNT_MAX,
                        metadata_block                          = True,
                        metadata_length                         = METADATA_LENGTH_MAX,
                   ),
                   getVBytes_NFTOutput(
                        weight_key                              = WEIGHT_KEY,
                        weight_data                             = WEIGHT_DATA,
                        additional_name                         = "min functionality",
                        output_size_max                         = output_size_max,
                        metadata_length_max                     = METADATA_LENGTH_MAX,
                        native_token_count                      = 0,
                        immutable_metadata_length               = 0,
                        dust_deposit_return_unlock_condition    = False,
                        timelock_unlock_condition               = False,
                        expiration_unlock_condition             = False,
                        sender_block                            = False,
                        issuer_block                            = False,
                        tag_block                               = False,
                        metadata_block                          = False,
                        metadata_length                         = 0,
                   ),
                   getVBytes_NFTOutput(
                        weight_key                              = WEIGHT_KEY,
                        weight_data                             = WEIGHT_DATA,
                        additional_name                         = "max functionality",
                        output_size_max                         = output_size_max,
                        metadata_length_max                     = METADATA_LENGTH_MAX,
                        native_token_count                      = NATIVE_TOKEN_COUNT_MAX,
                        immutable_metadata_length               = METADATA_LENGTH_MAX,
                        dust_deposit_return_unlock_condition    = True,
                        timelock_unlock_condition               = True,
                        expiration_unlock_condition             = True,
                        sender_block                            = True,
                        issuer_block                            = True,
                        tag_block                               = True,
                        metadata_block                          = True,
                        metadata_length                         = METADATA_LENGTH_MAX,
                   ),                   
    ]:
        vbytes.summary()
