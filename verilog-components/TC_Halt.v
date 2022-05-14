module TC_Halt (en);
    parameter UUID = 0;
    parameter NAME = "";
    parameter HALT_MESSAGE = "";
    input en;
    
    always @ (posedge en) begin
        $display(HALT_MESSAGE);
        $stop;
    end
endmodule
