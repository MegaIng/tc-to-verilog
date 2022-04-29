module TC_Hdd (clk, rst, seek, load, save, in, out);
    parameter MEM_WORDS = 256;
    input clk;
    input rst;
    input [63:0] seek;
    input load;
    input save;
    input [63:0] in;
    output tri0 [63:0] out;
    
    reg [63:0] mem [0:MEM_WORDS-1];
    reg [63:0] outval;
    reg [63:0] mp;
    
    always @ (posedge clk or rst) begin
        if (rst) begin
            mp = {64{1'bZ}};
            outval = {64{1'bZ}};
        end else begin
            mp <= mp + seek;
            if (load) begin
                outval <= mem[mp];
            end
        end
    end
    
    always @ (posedge clk or rst) begin
        if (save && !rst) begin
            mem[mp] <= in;
        end
    end
    
    assign out = outval;
endmodule
